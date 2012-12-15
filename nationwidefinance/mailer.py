
from django.template.loader import get_template
from django.contrib.sites.models import Site
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

def send_new_user_email(referrer=None, referred=None, business_name=None):
    t = get_template('new_referrer_email.html')

    site = Site.objects.get_current()

    c1 = Context(dict(user = referrer, business_name = business_name, site = site))
    c2 = Context(dict(user = referred, business_name = business_name, site = site))

    body1 = t.render(c1)
    body2 = t.render(c2)

    subject = 'Welcome to Nationwide Finance'

    if not referrer.is_active: send_email(subject=subject, body=body1, to_email=[referrer.email])
    if not referred.is_active: send_email(subject=subject, body=body2, to_email=[referred.email])

