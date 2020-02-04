from django import template
import json

register = template.Library()

@register.filter
def pretty_json(value):
    return json.dumps(json.loads(value), indent=2)
