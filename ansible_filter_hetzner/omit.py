#!/usr/bin/python

from ansible_filter_hetzner.helpers import filter_dict, filter_list, TYPE_OMIT


def omit(obj, attributes):
    if isinstance(obj, dict):
        return filter_dict(obj, attributes, TYPE_OMIT)
    elif isinstance(obj, list):
        return filter_list(obj, attributes, TYPE_OMIT)

    raise TypeError('Given object is whether a dictionary nor a list.')
