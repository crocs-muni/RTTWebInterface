from django import template
import json
from collections import OrderedDict
import logging
from .jsonenc import NoIndent, IndentingJSONEncoder

logger = logging.getLogger(__name__)
register = template.Library()


def noindent_poly_key(key, val, fnc):
    if key != "poly":
        return fnc(val)
    return NoIndent(val)


def noindent_poly(val):
    if isinstance(val, list):
        return [noindent_poly(x) for x in val]
    elif isinstance(val, tuple):
        return tuple([noindent_poly(x) for x in val])
    elif isinstance(val, OrderedDict):
        return OrderedDict([(x, noindent_poly_key(x, val[x], noindent_poly)) for x in val])
    elif isinstance(val, dict):
        return dict([(x, noindent_poly_key(x, val[x], noindent_poly)) for x in val])
    else:
        return val


@register.filter
def pretty_json(value):
    if not value:
        return value
    try:
        return json.dumps(json.loads(value, object_pairs_hook=OrderedDict), indent=2)
    except Exception as e:
        logger.info("Exception in JSON recoding: %s" % (e,), exc_info=e)
        return value


@register.filter
def pretty_json_booltest(value):
    if not value:
        return value
    try:
        js = noindent_poly(json.loads(value, object_pairs_hook=OrderedDict))
        return json.dumps(js, indent=2, cls=IndentingJSONEncoder)

    except Exception as e:
        logger.info("Exception in JSON recoding: %s" % (e,), exc_info=e)
        return value


@register.filter
def pretty_poly(value):
    if not value or isinstance(value, str):
        return value
    return json.dumps(value)
