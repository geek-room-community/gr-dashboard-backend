from flask import Flask, send_file
from flask_restful import Api
from routes import Dashboard, CertificateSender, Users, CertificatePreview
import os
from dotenv import load_dotenv
from models import db

#flask intialization
app = Flask(__name__)
api=Api(app)

#database config


db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise ValueError("DATABASE_URL is not set or improperly configured in the .env file.")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv("TRACK_MODIFICATION")

db.init_app(app)
#flask_restful routes
api.add_resource(Dashboard, '/')
api.add_resource(CertificateSender,"/certificate-sender")
api.add_resource(Users, '/users')
api.add_resource(CertificatePreview, "/certificate-preview")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates tables in the configured database if they don't already exist
        print("Database initialized.")
    app.run(debug=True) 
