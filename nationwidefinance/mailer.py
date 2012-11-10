from django.template.loader import get_template
from django.template import Context
from django.core import mail
from django.conf import settings


def send_email(subject=None, body=None, to_email=None, fail_silently=False):
	params = dict(
        subject = subject,
        body = body,
        from_email = 'admin@webiken.net',
        to = to_email,
    )
                
    try:
        connection = mail.get_connection(fail_silently=fail_silently)
        connection.open()
        email = mail.EmailMessage(**params)
        email.content_subtype = "html"
        email.send()
        connection.close()
    except ValueError, e:
        raise ValueError('Invalid backend argument')