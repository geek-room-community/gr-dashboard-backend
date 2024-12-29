from flask import Flask, send_file
from flask_cors import CORS
from flask_restful import Api
from routes import Dashboard, CertificateSender, Users, CertificatePreview
import os
from dotenv import load_dotenv
from models import db

# Load environment variables from .env file
load_dotenv()

# Flask initialization
app = Flask(__name__)
api = Api(app)

# Database config
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise ValueError("DATABASE_URL is not set or improperly configured in the .env file.")
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv("TRACK_MODIFICATION", "False")  # Default to False

db.init_app(app)

# Flask-RESTful routes
api.add_resource(Dashboard, '/')
api.add_resource(CertificateSender, "/certificate-sender")
api.add_resource(Users, '/users')
api.add_resource(CertificatePreview, "/certificate-preview")

# Add CORS protection using Flask-CORS
CORS(app, resources={r"/*": {"origins": f"{os.getenv('FRONTEND_URL')}/*"}})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates tables in the configured database if they don't already exist
        print("Database initialized.")
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 for local development
    app.run(host='0.0.0.0', port=port, debug=True)  # Bind to all interfaces
