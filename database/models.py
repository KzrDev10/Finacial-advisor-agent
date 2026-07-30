from sqlalchemy.orm import backref
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(20),primary_key=True,nullable=False)
    age = db.Column(db.Integer,nullable=False)
    current_savings = db.Column(db.Float,nullable=False,default=0.0)
    monthly_contribution = db.Column(db.Float,nullable=False,default=0.0)
    risk_tolerance = db.Column(db.String(13),nullable=True)

    goals = db.relationship('SavingsGoal',backref='user',lazy=True)

class SavingsGoal(db.Model):
    __tablename__ = 'savings_goals'
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    goal_name= db.Column(db.String(30),nullable=False)
    target_amount = db.Column(db.Float,nullable=False)
    timeline_months = db.Column(db.Integer,nullable=False)
    user_id = db.Column(db.String(20),db.ForeignKey('users.id'),nullable=False)