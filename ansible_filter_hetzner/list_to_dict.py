#!/usr/bin/python

from ansible_filter_hetzner.helpers import array_to_dict as list_to_dict


class FilterModule(object):

    def filters(self):
        return {
            'hetzner_list_to_dict': list_to_dict
        }
