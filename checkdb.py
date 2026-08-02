from app import app
from database.models import db, User

# Wake up the Flask application context
with app.app_context():
    # Fetch every user in the database
    all_users = User.query.all()
    
    print(f"--- Found {len(all_users)} users in the database ---")
    
    for user in all_users:
        print(f"Name: {user.first_name} {user.last_name} | Email: {user.email}")