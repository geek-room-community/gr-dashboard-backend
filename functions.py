import os
import base64
import logging
import io
import cv2
import requests
from dotenv import load_dotenv
from PIL import Image
import numpy as np
load_dotenv()

# Configure logging
logging.basicConfig(filename='certificate_process.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def generate_preview(image_byte, full_name="John Doe", about_text=((600, 600), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 0), 3)):
    try:
        cords, font, size, color, thickness = about_text[0], about_text[
            1], about_text[2], about_text[3], about_text[4]
        # Convert byte stream to a NumPy array
        nparr = np.frombuffer(image_byte, np.uint8)
        # Decode NumPy array into an image
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # Overlay the text
        image = cv2.putText(image, full_name, cords, font,
                            size, color, thickness)
        # Encode the modified image back to bytes
        _, image_data = cv2.imencode('.jpg', image)
        logging.info("Preview generated")
        return image_data.tobytes()
    except Exception as e:
        logging.error(f"Error generating preview for {full_name}: {e}")
        return None


def process_and_send_certificate(image_byte, full_name, email, subject, body, about_text=((600, 600), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 0), 3)):
    # about_text should be a tuple with 4 elements, co-ordinates, font, size and color in this order
    try:
        cords, font, size, color, thickness = about_text[0], about_text[
            1], about_text[2], about_text[3], about_text[4]
        # Convert byte stream to a NumPy array
        nparr = np.frombuffer(image_byte, np.uint8)
        # Decode NumPy array into an image
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.putText(image, full_name, cords,
                            font, size, color, thickness)

        # Converting image to pdf
        pil_image = Image.fromarray(image)
        pdf_buffer = io.BytesIO()
        pil_image.save(pdf_buffer, format="PDF")
        pdf_blob = pdf_buffer.getvalue()
        pdf_buffer.close()

        # Send email with the attached PDF
        send_email(full_name, email, subject, body, pdf_blob)
    except Exception as e:
        logging.error(f"Error processing {full_name} ({email}): {e}")

# Function to send an email with an attachment


def send_email(full_name, email, subject, body, pdf_blob):
    url = 'https://api.emailit.com/v1/emails'

    headers = {
        "Authorization": f"Bearer {os.getenv('EMAILIT_API_KEY')}",
        "Content-Type": "application/json"
    }
    encoded_pdf = base64.b64encode(pdf_blob).decode('utf-8')

    email_data = {
        "from": os.getenv("EMAIL_ADDRESS"),
        "to": email,
        "subject": subject,
        "html": body,
        "attachments": [
            {
                "filename": f"{full_name}_Certificate.pdf",
                "content": encoded_pdf,
                "content_type": "base64"
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers,
                                 json=email_data, timeout=10)
        if response.status_code == 200:
            logging.info(f"Email sent successfully to {full_name} ({email})")
        else:
            logging.error(f"Failed to send email to {email}: {response.text}")
            raise Exception(f"Error sending email: {response.text}")
    except Exception as e:
        logging.error(f"Error processing email for {full_name} ({email}): {e}")
        raise Exception(f"Error sending email for {full_name} ({email}): {e}")
