from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    """This function is used to send emails asynchronously
    Note, for bulk emails using celery task queue is recommended"""
    app = current_app._get_current_object()  # Get the actual Flask app object
    msg = Message(current_app.config['UNITED_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=current_app.config['UNITED_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

def send_email_2(to, subject, template, **kwargs):
    """This function is used to send emails asynchronously
    Note, for bulk emails using celery task queue is recommended"""
    app = current_app._get_current_object()  # Get the actual Flask app object
    msg = Message(current_app.config['UNITED_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=current_app.config['UNITED_MAIL_SENDER'], recipients=[to])
    msg.body = template
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr