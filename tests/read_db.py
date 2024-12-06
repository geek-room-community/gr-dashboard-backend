"""
Run this file from root directory using the command
python -m tests.read_db
"""

from app import app, db
from models import User
from sqlalchemy import text  

def test_database():
    with app.app_context():
        try:
            with db.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                print("Database connection successful.")

            users = User.query.all()
            if not users:
                print("No users found in the database.")
            else:
                print("Users in the database:")
                for user in users:
                    print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")

        except Exception as e:
            print("An error occurred while accessing the database:", str(e))

if __name__ == "__main__":
    test_database()