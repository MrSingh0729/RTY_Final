from flask import Blueprint, jsonify, request
from flask_login import login_required
from models import ProjectGoal

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/project-goal')
@login_required
def get_project_goal():
    project_name = request.args.get('project')
    
    if not project_name:
        return jsonify({"error": "Project name is required"}), 400
    
    try:
        project_goal = ProjectGoal.query.filter_by(project_name=project_name).first()
        
        if project_goal:
            return jsonify({"goal": project_goal.goal})
        else:
            return jsonify({"goal": None})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
    
