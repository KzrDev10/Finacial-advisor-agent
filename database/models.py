from sqlalchemy.orm import backref
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(20), primary_key=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    current_savings = db.Column(db.Float, nullable=False, default=0.0)
    monthly_contribution = db.Column(db.Float, nullable=False, default=0.0)
    risk_tolerance = db.Column(db.String(13), nullable=True)

    goals = db.relationship('SavingsGoal', backref='user', lazy=True)

    def set_password(self, password):
        """Hash and store the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Return True if the plaintext password matches the stored hash."""
        return check_password_hash(self.password_hash, password)



class SavingsGoal(db.Model):
    __tablename__ = 'savings_goals'
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    goal_name= db.Column(db.String(30),nullable=False)
    target_amount = db.Column(db.Float,nullable=False)
    timeline_months = db.Column(db.Integer,nullable=False)
    user_id = db.Column(db.String(20),db.ForeignKey('users.id'),nullable=False)