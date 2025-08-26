from flask import Flask, render_template, request, send_file, jsonify, Blueprint, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import pandas as pd
import io
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from datetime import datetime, timedelta
import os
import json
import threading
import atexit  # Added this import
from apscheduler.schedulers.background import BackgroundScheduler
from utils.api import *
from utils.helpers import *
from config import Config
from routes import auth_bp, dashboard_bp, api_bp
from extensions import db
from models import FPYAutoData

# Initialize Flask App
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fpy_dashboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

# User class for authentication
class User:
    def __init__(self, id):
        self.id = id
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Add context processor to make datetime, Config, and column_headers available to templates
@app.context_processor
def inject_variables():
    column_headers = {
        "project": "Model",
        "station": "Station",
        "inPut": "Input Qty",
        "pass": "Good Qty",
        "fail": "NG",
        "notFail": "NDF",
        "der": "NG Rate",
        "ntf": "NDF Rate",
        "rty": "RTY",
        "py": "PY"
    }
    return dict(datetime=datetime, Config=Config, column_headers=column_headers)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(api_bp)

# Background scheduler for auto data refresh
scheduler = BackgroundScheduler()

def fetch_and_store_auto_data():
    """Function to fetch and store auto data"""
    try:
        with app.app_context():
            print(f"[{datetime.now()}] Starting auto data refresh...")
            
            # Get token
            token = get_token()
            
            # Get project list
            projects = get_project_list(token)
            
            # Get today's data from 08:00AM to now
            now = datetime.now()
            start = now.replace(hour=8, minute=0, second=0, microsecond=0)
            
            # Get FPY data
            fpy_data_raw = get_fpy(token, projects, start, now)
            
            # Process data
            desired_columns = ["project", "station", "inPut", "pass", "fail", "notFail", "der", "ntf", "rty", "py"]
            processed_data = []
            
            for row in fpy_data_raw:
                # Add PY column (empty for now)
                row["py"] = ""
                processed_data.append({col: row.get(col, "") for col in desired_columns})
            
            # Store data in database
            # First, clear existing data
            FPYAutoData.query.delete()
            
            # Then add new data
            for record in processed_data:
                auto_data = FPYAutoData(
                    project=record.get("project"),
                    station=record.get("station"),
                    inPut=record.get("inPut"),
                    pass_qty=record.get("pass"),
                    fail=record.get("fail"),
                    notFail=record.get("notFail"),
                    der=record.get("der"),
                    ntf=record.get("ntf"),
                    rty=record.get("rty"),
                    py=record.get("py"),
                    last_updated=datetime.now()
                )
                db.session.add(auto_data)
            
            db.session.commit()
            print(f"[{datetime.now()}] Auto data refresh completed. {len(processed_data)} records stored.")
            
    except Exception as e:
        print(f"[{datetime.now()}] Error in auto data refresh: {str(e)}")
        import traceback
        traceback.print_exc()

# Schedule the job to run every 15 minutes
scheduler.add_job(
    func=fetch_and_store_auto_data,
    trigger="interval",
    minutes=15,
    id='auto_data_refresh_job',
    name='Refresh auto data every 15 minutes',
    replace_existing=True
)

# Start the scheduler
scheduler.start()

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    current_time = datetime.now().strftime('%H:%M')
    return render_template('errors/404.html', current_time=current_time), 404

@app.errorhandler(500)
def internal_server_error(e):
    current_time = datetime.now().strftime('%H:%M')
    return render_template('errors/500.html', error=str(e), current_time=current_time), 500

# Make sure to shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())




@app.route('/')
def root():
    return redirect(url_for('dashboard.home'))

# Main entry point
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)