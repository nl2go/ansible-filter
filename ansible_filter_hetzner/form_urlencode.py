#!/usr/bin/python

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote


def form_urlencode(obj, is_root=True, namespace=''):
    encoded_str = ''

    if isinstance(obj, list):
        for i in range(len(obj)):
            separator = get_separator(obj[i])
            entry_namespace = namespace + get_namespace(str(i), is_root) + separator
            encoded_str = encoded_str + form_urlencode(obj[i], False, entry_namespace)
    elif isinstance(obj, dict):
        for key in obj:
            separator = get_separator(obj[key])
            entry_namespace = namespace + get_namespace(key, is_root) + separator
            encoded_str = encoded_str + form_urlencode(obj[key], False, entry_namespace)
    else:
        encoded_str = encoded_str + namespace + serialize_value(obj) + "&"

    return encoded_str


def get_separator(value):
    is_object = isinstance(value, list) or isinstance(value, dict)
    if is_object:
        return ''
    else:
        return '='


def get_namespace(key, is_root):
    if is_root:
        template = "{0}"
    else:
        template = "[{0}]"

    return template.format(key)


def serialize_value(obj):
    if isinstance(obj, bool):
        result = str(obj).lower()
    elif obj is None:
        result = 'null'
    else:
        result = quote(str(obj))

    return result
