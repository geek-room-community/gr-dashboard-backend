import cv2
import numpy as np
from email.mime.multipart import MIMEMultipart
import os
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import pandas as pd
from PIL import Image
import io
import smtplib
from dotenv import load_dotenv
import logging
load_dotenv()

# Configure logging
logging.basicConfig(filename='certificate_process.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def generate_preview(image_byte, full_name, about_text = ((600, 600), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (0, 0, 0))):
    try:
        cords, font, size, color = about_text[0], about_text[1], about_text[2], about_text[3]
        # Convert byte stream to a NumPy array
        nparr = np.frombuffer(image_byte, np.uint8)
        # Decode NumPy array into an image
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image = cv2.putText(image, full_name, cords, font, size, color)
        _, image_data = cv2.imencode('.jpg', image)
    except Exception as e:
        logging.error(f"Error generating preview for {full_name}: {e}")
        image_data=None
    finally:
        return image_data

def process_and_send_certificate(image_byte, row, subject, body, about_text = ((600, 600), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (0, 0, 0))):
    #about_text should be a tuple with 4 elements, co-ordinates, font, size and color in this order
    try:
        full_name = row['Full Name']
        email = row['Email']
        cords, font, size, color = about_text[0], about_text[1], about_text[2], about_text[3]
        
        # Convert byte stream to a NumPy array
        nparr = np.frombuffer(image_byte, np.uint8)
        # Decode NumPy array into an image
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.putText(image, full_name, cords, font, size, color)

        # Converting image to pdf
        pil_image = Image.fromarray(image)
        pdf_buffer = io.BytesIO()
        pil_image.save(pdf_buffer, format="PDF")
        pdf_blob = pdf_buffer.getvalue()
        pdf_buffer.close()
    
        # Send email with the attached PDF
        msg = MIMEMultipart()
        msg['From'] = os.getenv("EMAIL_ADDRESS")
        msg['To'] = email
        msg['Subject'] = subject
        if pd.notna(full_name) and pd.notna(email): 
            email_body = body.replace("{Full_Name}", full_name)
        msg.attach(MIMEText(email_body, 'html'))

        pdf_attachment = MIMEApplication(pdf_blob, Name=f"{full_name}_Certificate.pdf")
        pdf_attachment['Content-Disposition'] = f'attachment; filename="{full_name}_Certificate.pdf"'
        msg.attach(pdf_attachment)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
            server.send_message(msg)
        return f"Certificate sent successfully to {full_name} ({email})"
    except Exception as e:
            logging.error(f"Error processing {full_name} ({email}): {e}")
            return f"Error processing {full_name} ({email}): {e}"

"""
This code was used to check the working of these functions without the use of flask, directly in the terminal
# Example byte stream (e.g., from a file or network request)
with open('tests\\test.jpg', 'rb') as f:
    image_byte = f.read()

row = {'Full Name': "Jaspreet Singh", 'Email': "jaspreet.jsk.kohli@gmail.com"}
#process_and_send_certificate(image_byte, row, "Certificate of Achievement", "Hello Jaspreet Singh, congratulations! 🎉")

nparr = np.frombuffer(generate_preview(image_byte, "Jaspreet Singh"), np.uint8)
image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""