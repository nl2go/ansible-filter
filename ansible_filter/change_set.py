#!/usr/bin/python

import copy

from ansible_filter.helpers import array_to_dict

STATE_KEY = 'state'
STATE_PRESENT = 'present'
STATE_ABSENT = 'absent'

ACTION_KEY = 'action'
ACTION_CREATE = 'create'
ACTION_UPDATE = 'update'
ACTION_NOOP = 'noop'
ACTION_DELETE = 'delete'

OBJ_KEY = 'value'


def dict_to_array(obj_dict):
    obj_array = []

    for obj_key, obj_value in obj_dict.items():
        obj_array.append(obj_value)

    return obj_array


def get_action(local_obj, origin_obj, state, origin_default):
    if not origin_obj:
        result = ACTION_CREATE if state == STATE_PRESENT else ACTION_NOOP
    elif is_equal_obj(local_obj, origin_obj):
        result = ACTION_NOOP if state == STATE_PRESENT or is_equal_obj(origin_default, origin_obj) else ACTION_DELETE
    else:
        result = ACTION_UPDATE if state == STATE_PRESENT else ACTION_DELETE

    return result


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def is_equal_obj(local_obj, origin_obj):
    result = None

    if is_all_empty(local_obj, origin_obj):
        result = True
    elif is_any_bool(local_obj, origin_obj):
        result = is_equal_bool(local_obj, origin_obj)
    elif is_all_dict(local_obj, origin_obj):
        result = is_equal_dict(local_obj, origin_obj)
    elif is_list(local_obj) and is_list(origin_obj):
        result = is_equal_list(local_obj, origin_obj)
    elif local_obj != origin_obj:
        result = False

    return True if result is None else result


def is_equal_bool(left, right):
    if not isinstance(left, bool):
        left = str2bool(left)
    if not isinstance(right, bool):
        right = str2bool(right)
    return left is right


def is_equal_list(left, right):
    if len(left) != len(right):
        return False

    for i in range(len(left)):
        local_value = left[i]
        origin_value = right[i]
        if not is_equal_obj(local_value, origin_value):
            return False

    return True


def is_equal_dict(left, right):
    for key, local_value in left.items():
        origin_value = right.get(key)
        if not is_equal_obj(local_value, origin_value):
            return False

    return True


def is_any_bool(left, right):
    return isinstance(left, bool) or isinstance(right, bool)


def is_all_empty(left, right):
    return is_empty(left) and is_empty(right)


def is_all_dict(left, right):
    return is_dict(left) and is_dict(right)


def is_all_list(left, right):
    return is_list(left) and is_list(right)


def is_dict(obj):
    return isinstance(obj, dict)


def is_list(obj):
    return isinstance(obj, list)


def is_empty(value):
    if value:
        return False
    return True


def remove_state(obj):
    return obj.pop(STATE_KEY, STATE_PRESENT)


def update_obj(obj, origin_obj):
    if origin_obj:
        updated_obj = copy.deepcopy(origin_obj)
        updated_obj.update(obj)
    else:
        updated_obj = obj

    return updated_obj


def change_set(local, origin, origin_default=None, attr='name'):
    result_dict = {
        ACTION_CREATE: [],
        ACTION_UPDATE: [],
        ACTION_DELETE: [],
        ACTION_NOOP: []
    }

    if not local:
        return result_dict

    if is_dict(local):
        origin = {} if not is_dict(origin) else origin
        change_set_item(result_dict, local, origin, origin_default)

        return result_dict

    if is_list(local):
        local_dict = array_to_dict(local, attr)
        origin_dict = {} if not is_list(origin) else array_to_dict(origin, attr)
        change_set_items(result_dict, local_dict, origin_dict, origin_default)

        return result_dict

    raise TypeError('Can not build change set for given objects: ' + str(local) + ", " + str(origin))


def change_set_item(result_dict, local_obj, origin_obj, origin_default):
    obj = copy.deepcopy(local_obj)
    state = remove_state(obj)
    action = get_action(obj, origin_obj, state, origin_default)

    obj = update_obj(obj, origin_obj)
    result_dict[action].append(obj)


def change_set_items(result_dict, local_dict, origin_dict, origin_default):
    for obj_key, local_obj in local_dict.items():
        origin_obj = origin_dict.get(obj_key)
        change_set_item(result_dict, local_obj, origin_obj, origin_default)
