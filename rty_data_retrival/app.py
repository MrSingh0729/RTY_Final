from flask import Flask, render_template, request, send_file, jsonify, Blueprint
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import pandas as pd
import io
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from datetime import datetime
import os
from utils.api import *
from utils.helpers import *
from config import Config
import json
from routes import auth_bp, dashboard_bp, api_bp

# Initialize Flask App
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")

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

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(api_bp)

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html', error=str(e)), 500

# Main entry point
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)