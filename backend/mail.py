import smtplib
import secrets
from email.mime.text import MIMEText


def send_auth_mail_to_reset_password(client_email):
    gmail_user = 'wawid.dolszczak@gmail.com'
    gmail_password = 'jjjrilvsllgsbeqg'
    to = str(client_email)
    subject = 'DataRoom Password Reset'
    token = secrets.token_hex(10)
    body = 'Click on this link to restart your password https://dataroom-301309.ew.r.appspot.com/mail/{}/{}'.format(client_email, token)
    message = MIMEText(body)

    message = "From: {}\nTo: {}\nSubject: {}\n{}\n".format(gmail_user, to, subject, message)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to, message)
        server.close()
        return token
    except:
        return False


def send_mail_with_new_password(client_email, new_password):
    gmail_user = 'wawid.dolszczak@gmail.com'
    gmail_password = 'jjjrilvsllgsbeqg'
    to = client_email
    subject = 'DataRoom New Password'
    body = 'Your new password is: {}'.format(new_password)
    message = MIMEText(body)

    message = "From: {}\nTo: {}\nSubject: {}\n{}\n".format(gmail_user, to, subject, message)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to, message)
        server.close()
        return True
    except:
        return False