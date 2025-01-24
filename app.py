from flask import Flask, send_file
from flask_restful import Api
from routes import Dashboard, CertificateSender, Users, CertificatePreview
import os
from dotenv import load_dotenv
from models import db
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

# Flask initialization
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = None  # 16 MB
app.config['MAX_FORM_MEMORY_SIZE'] = 50 * 1024 * 1024  # 50 MB
CORS(app, resources={
     r"/certificate-preview": {"origins": "https://dashboards.geekroom.in"},
     r"/certificate-sender": {"origins": "https://dashboards.geekroom.in"}})
api = Api(app)

# Database config
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise ValueError(
        "DATABASE_URL is not set or improperly configured in the .env file.")
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv(
    "TRACK_MODIFICATION", "False")  # Default to False

db.init_app(app)

# Flask-RESTful routes
api.add_resource(Dashboard, '/')
api.add_resource(CertificateSender, "/certificate-sender")
api.add_resource(Users, '/users')
api.add_resource(CertificatePreview, "/certificate-preview")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates tables in the configured database if they don't already exist
        print("Database initialized.")
    # Default to 5000 for local development
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)  # Bind to all interfaces
