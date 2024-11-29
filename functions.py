import smtplib
from email.message import EmailMessage
import pandas as pd

MY_EMAIL = "bhatiaudit55@gmail.com"
PASSWORD = ""  # Enter your email password or app-specific password here

def send_mail(full_name, user_email, subject, body, pdf_blob):
    user_mail = user_email
    msg = EmailMessage()
    msg['From'] = MY_EMAIL
    msg['To'] = user_mail
    msg['Subject'] = subject
    msg.set_content(f"Hey {full_name},\n\n{body}")

    # Attach the PDF
    msg.add_attachment(
        pdf_blob, 
        maintype='application', 
        subtype='pdf', 
        filename=f"{full_name}_Certificate.pdf"
    )

    # Send the email
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.send_message(msg)

def process_certificates(sheet_data, presentation_id, subject, body):
    global drive_service, slides_service  # Declare global before use
    num_rows = len(sheet_data)

    for index, row in sheet_data.iterrows():
        full_name = row['Full Name']
        email = row['Email']
        email_body = body.replace("{Full_Name}", full_name)

        if pd.notna(full_name) and pd.notna(email):
            # Create a copy of the presentation
            presentation_copy = drive_service.files().copy(
                fileId=presentation_id,
                body={'name': f'{full_name} Presentation'}
            ).execute()
            copied_presentation_id = presentation_copy['id']

            # Replace placeholders in the copied presentation
            requests = [{
                'replaceAllText': {
                    'containsText': {
                        'text': '{{Full_Name}}',
                        'matchCase': True
                    },
                    'replaceText': full_name
                }
            }]
            slides_service.presentations().batchUpdate(
                presentationId=copied_presentation_id,
                body={'requests': requests}
            ).execute()

            # Export as PDF
            pdf_blob = drive_service.files().export(
                fileId=copied_presentation_id,
                mimeType='application/pdf'
            ).execute()

            # Send email with the attached PDF
            send_mail(full_name, email, subject, email_body, pdf_blob)

            # Delete the copied presentation
            drive_service.files().delete(fileId=copied_presentation_id).execute()

