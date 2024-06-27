import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
from typing import Final

with open('configs/email.json', 'r') as config_file:
    config = json.load(config_file)

async def send_email(subject, body, to_email):
    SERVER: Final = config['SMTP_SERVER']
    PORT: Final = config['SMTP_PORT']
    EMAIL: Final = config['SENDER_EMAIL']
    PASS: Final = config['SENDER_PASSWORD']
    smtp_server = SERVER
    smtp_port = PORT
    sender_email = EMAIL
    sender_password = PASS

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))
    server = smtplib.SMTP(smtp_server, smtp_port)

    try:
        server.starttls() 
        server.login(sender_email, sender_password)

        server.send_message(msg)
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        server.quit()
