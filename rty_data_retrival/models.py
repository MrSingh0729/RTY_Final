from extensions import db
from datetime import datetime

class ModelDescription(db.Model):
    __tablename__ = 'model_description'
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(100), unique=True, nullable=False)
    technology = db.Column(db.String(50))
    position = db.Column(db.String(50))
    brand = db.Column(db.String(50))
    goal = db.Column(db.String(10))  # e.g., "93%"

class ProjectGoal(db.Model):
    __tablename__ = 'project_goal'
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), unique=True, nullable=False)
    goal = db.Column(db.String(10))  # e.g., "93%"

class FPYData(db.Model):
    __tablename__ = 'fpy_data'
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(100), nullable=False)
    station = db.Column(db.String(50), nullable=False)
    inPut = db.Column(db.Integer, nullable=False)
    pass_qty = db.Column(db.Integer, nullable=False)  # Changed from 'pass' to 'pass_qty'
    fail = db.Column(db.Integer, nullable=False)
    notFail = db.Column(db.Integer, nullable=False)
    der = db.Column(db.Float)  # NG Rate
    ntf = db.Column(db.Float)  # NDF Rate
    rty = db.Column(db.Float)  # RTY
    py = db.Column(db.Float)  # PY
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class FPYAutoData(db.Model):
    __tablename__ = 'fpy_auto_data'
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(100), nullable=False)
    station = db.Column(db.String(50), nullable=False)
    inPut = db.Column(db.Integer, nullable=False)
    pass_qty = db.Column(db.Integer, nullable=False)
    fail = db.Column(db.Integer, nullable=False)
    notFail = db.Column(db.Integer, nullable=False)
    der = db.Column(db.Float)  # NG Rate
    ntf = db.Column(db.Float)  # NDF Rate
    rty = db.Column(db.Float)  # RTY
    py = db.Column(db.Float)  # PY
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)