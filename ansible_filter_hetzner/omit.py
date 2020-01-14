#!/usr/bin/python

from ansible_filter_hetzner.helpers import filter_object, TYPE_OMIT


def omit(obj, attributes):
    return filter_object(obj, attributes, TYPE_OMIT)
