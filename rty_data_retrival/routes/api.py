from flask import Blueprint, jsonify
from flask_login import login_required
from datetime import datetime
from utils.api import get_token, get_project_list

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/health')
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@api_bp.route('/projects')
@login_required
def get_projects():
    try:
        token = get_token()
        projects = get_project_list(token)
        return jsonify({"projects": projects})
    except Exception as e:
        return jsonify({"error": str(e)}), 500