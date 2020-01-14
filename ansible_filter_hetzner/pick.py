#!/usr/bin/python

from ansible_filter_hetzner.helpers import filter_dict, filter_list, TYPE_PICK


def pick(obj, attributes):
    if isinstance(obj, dict):
        return filter_dict(obj, attributes, TYPE_PICK)
    elif isinstance(obj, list):
        return filter_list(obj, attributes, TYPE_PICK)

    raise TypeError('Given object is neither a dictionary nor a list.')
