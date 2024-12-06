"""
Run this file from root directory using the command
python -m tests.delete_db
"""
from app import app, db
from models import User
from sqlalchemy import text

def delete_all_entries():
    with app.app_context():
        try:
            # Delete all records in the User table
            deleted_rows = User.query.delete()  # Returns the number of rows deleted
            db.session.commit()  # Commit the changes to the database
            print(f"Deleted {deleted_rows} rows from the User table.")
            
            # Reset auto-increment counter for the 'users' table (PostgreSQL specific)
            db.session.execute(text("ALTER SEQUENCE users_id_seq RESTART WITH 1"))
            db.session.commit()
            print("Auto-increment counter reset for 'users' table.")

        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            print(f"An error occurred while deleting entries: {str(e)}")

if __name__ == "__main__":
    delete_all_entries()