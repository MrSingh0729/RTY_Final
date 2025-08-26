from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from config import Config
 
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
 
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
 
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple authentication - in production, use proper authentication
        if username == Config.USER_CODE and password == Config.PASSWORD:
            user = User(username)
            login_user(user)
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid credentials', 'danger')
            return render_template('auth/login.html', error='Invalid credentials')
    
    return render_template('auth/login.html')
 
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))