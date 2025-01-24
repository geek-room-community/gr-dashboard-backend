import io
import base64
import json
from flask_restful import Resource
from flask import request, send_file, jsonify
from PIL import Image
import pandas as pd
from models import db, User
from functions import generate_preview, process_and_send_certificate

# mainpage dashboard


class Dashboard(Resource):
    def get(self):
        return {"message": "Geek Room Dashboard!"}

# certificate Sender


class CertificateSender(Resource):
    def get(self):
        return {"message": "Certificate Sender"}

    def post(self):
        try:
            if "file" not in request.files:
                return jsonify({"error": "No file part"}), 400

            csv_file = request.files["file"]
            csv_data = io.BytesIO(csv_file.read())
            df = pd.read_csv(csv_data)

            img_file = request.form['image']

            # Read the uploaded image as bytes
            image_bytes = base64.b64decode(img_file.split(',')[1])

            image = Image.open(
                io.BytesIO(base64.b64decode(img_file.split(',')[1])))

            width, height = image.size

            start_x = float(request.form['start'])
            start_y = float(request.form['end'])
            font = int(request.form['font'])
            size = float(request.form['size'])
            color = json.loads(request.form['color'])
            thickness = int(request.form['thickness'])
            about_text = ((int(start_x*width), int(start_y*height)),
                          font, size, color, thickness)
            subject = request.form['subject']
            body = request.form['body']

            # Process and send certificates for each user
            for i in range(len(df.index)):
                full_name = df.loc[i].iloc[0]
                email = df.loc[i].iloc[1]
                process_and_send_certificate(
                    image_bytes, full_name, email, subject, body, about_text)

                existing_user = User.query.filter(
                    (User.email == email)).first()

                if existing_user:
                    continue
                # Add user to the database
                user = User(username=full_name, email=email)
                db.session.add(user)

            # Committing all database changes
            db.session.commit()

            return {"message": "Certificates processed successfully"}, 200

        except Exception as e:
            # Rolling back in case of an error
            db.session.rollback()
            return {"error": str(e)}, 500

# preview shower


class CertificatePreview(Resource):
    def post(self):
        try:
            img_file = request.form['image']

            # Read the uploaded image as bytes
            image_bytes = base64.b64decode(img_file.split(',')[1])

            image = Image.open(
                io.BytesIO(base64.b64decode(img_file.split(',')[1])))
            width, height = image.size

            start_x = float(request.form['start'])
            start_y = float(request.form['end'])
            font = int(request.form['font'])
            size = float(request.form['size'])
            color = json.loads(request.form['color'])
            thickness = int(request.form['thickness'])
            about_text = ((int(start_x*width), int(start_y*height)),
                          font, size, color, thickness)
            # Generate the certificate preview
            result = generate_preview(image_bytes, about_text=about_text)

            if result is None:
                return {"error": "Failed to generate certificate preview"}, 500

            # Return the modified image
            response = send_file(
                io.BytesIO(result),
                mimetype='image/jpeg',
                as_attachment=False,
                download_name='certificate_preview.jpg'
            )

            return response

        except Exception as e:
            return {"error": str(e)}, 500


# db connection checker
class Users(Resource):
    def get(self):
        try:
            users = User.query.all()
            # Format users as a list of dictionaries
            users_list = [{"id": user.id, "username": user.username,
                           "email": user.email} for user in users]
            return {"users": users_list}, 200

        except Exception as e:
            return {"error": str(e)}, 500
