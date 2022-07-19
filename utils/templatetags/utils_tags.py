from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag("utils/matomo_code.html", takes_context=True)
def tracking_code(context):
    return {
        "CSP_NONCE": context["CSP_NONCE"],
        "DISPLAY": not settings.DEBUG,
    }


@register.inclusion_tag("utils/matomo_event.html", takes_context=True)
def push_event(context, category, action, name):
    return {
        "CSP_NONCE": context["CSP_NONCE"],
        "CATEGORY": category,
        "ACTION": action,
        "NAME": name,
    }
