from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.model):
    __tablename__ == 'users'
    id = db.Column(db.String(20),primary_key=True,nullable=False)
    age = db.Column(db.Integer,nullable=False)
    current_savings = db.Column(db.Float,nullable=False,default=0.0)
    monthly_contribution = db.Column(db.Float,nullable=False,default=0.0)
    risk_tolerance = db.Column(db.String(13),nullable=True)