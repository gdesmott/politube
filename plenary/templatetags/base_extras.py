from django import template
from django.core.urlresolvers import resolve, Resolver404

register = template.Library()

@register.simple_tag(takes_context=True)
def navactive(context, views):
    request = context['request']
    try:
        view = resolve(request.path).url_name
        if view in views:
            return "active"
        else:
            return ""
    except Resolver404:
        return ""
