#!/usr/bin/python

from ansible_filter.helpers import array_to_dict


def group_by(lefts, rights, attr='name'):
    results = []
    rights_dict = array_to_dict(rights, attr)
    for left in lefts:
        key = left.get(attr)
        result = {attr: key, 'group': [left]}
        right = rights_dict.get(key)
        if right:
            result['group'].append(right)
            results.append(result)
    return results
