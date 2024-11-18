from flask import Flask
from flask_restful import Api
from routes import Dashboard, CertificateSender, Users
import os
from dotenv import load_dotenv
from models import db,User

#flask intialization
app = Flask(__name__)
api=Api(app)

#database config
load_dotenv()
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

#flask_restful routes
api.add_resource(Dashboard, '/')
api.add_resource(CertificateSender,"/certificate-sender")
api.add_resource(Users, '/users')

if __name__ == '__main__':
    with app.app_context():
        # Check if the database file exists
        if not os.path.exists('users.db'):
            db.create_all()  # Create tables only the first time
            print("Database created and tables initialized.")
    app.run(debug=True)
