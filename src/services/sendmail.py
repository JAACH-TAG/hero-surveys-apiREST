import os
import smtplib
from email.mime.text import MIMEText

def send_mail(name, email, comment):
    port = 2525
    smtp_sever = 'smtp.mailtrap.io'
    username = os.environ.get("MAIL_USERNAME")
    password = os.environ.get("MAIL_PASSWORD")
    message = f"<h3>New feedback submission</h3><ul> <li>name: {name}</li> <li>email: {email}</li> <li>comment: {comment}</li> </ul>"

    sender_email = email
    receiver_email = "herosurveys@site.com"
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Hero Surveys Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send Email
    with smtplib.SMTP(smtp_sever, port) as server:
        server.login(username, password)
        server.sendmail(sender_email, receiver_email, msg.as_string()) 


