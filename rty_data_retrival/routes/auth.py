from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from utils.api import get_token

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            # Try to authenticate with the API
            token = get_token()
            if token:
                # If successful, log in the user
                from app import User
                user = User(username)
                login_user(user)
                return redirect(url_for('dashboard.index'))
        except Exception as e:
            error = "Invalid username or password"
    
    return render_template('auth/login.html', error=error)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))