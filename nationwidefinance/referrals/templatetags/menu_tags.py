from django.core.urlresolvers import reverse
from django import template
register = template.Library()


@register.simple_tag(name='active')
def active(request, url_name):
    path = request.path
    if path == reverse(url_name):
        return 'current-menu-item current_page_item'
    return ''