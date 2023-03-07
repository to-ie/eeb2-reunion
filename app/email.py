from threading import Thread
from flask import render_template
from flask_mail import Message
from app import mail, app

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('EEB2 Reunion - Reset Your Password',
               sender='no-reply@t-o.ie',
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))

def send_verification_email(user, userid):
    send_email('EEB2 Reunion - Account verification',
               sender='no-reply@t-o.ie',
               recipients=[user.email],
               text_body=render_template('email/verification.txt',
                                         user=user, userid=userid),
               html_body=render_template('email/verification.html',
                                         user=user, userid=userid))

def send_contact_email(name, email, message, captcha):
    send_email('EEB2 Reunion - New message',
               sender='no-reply@t-o.ie',
               recipients=app.config['ADMINS'],
               text_body=render_template('email/contact.txt',
                                         name=name, email=email, message=message, captcha=captcha),
               html_body=render_template('email/contact.html',
                                         name=name, email=email, message=message, captcha=captcha))

def send_invite_email(email, captcha):
    send_email('EEB2 Reunion - Invitation',
               sender='no-reply@t-o.ie',
               recipients=[email],
               text_body=render_template('email/invite.txt',
                                         email=email, captcha=captcha),
               html_body=render_template('email/invite.html',
                                         email=email, captcha=captcha))