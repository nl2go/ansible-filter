TYPE_PICK = "pick"
TYPE_OMIT = "omit"


def array_to_dict(obj_array, attr='name'):
    obj_dict = {}

    for obj in obj_array:
        key = obj.get(attr)
        obj_dict[key] = obj

    return obj_dict


def filter_object(obj, attributes, filter_type):
    if isinstance(obj, dict):
        return filter_dict(obj, attributes, filter_type)
    elif isinstance(obj, list):
        return filter_list(obj, attributes, filter_type)

    raise TypeError('Given object is neither a dictionary nor a list.')


def filter_dict(obj_dict, attributes, filter_type):
    result_obj = {}
    for key, value in obj_dict.items():
        if filter_type == TYPE_OMIT and key not in attributes:
            result_obj[key] = value
        elif filter_type == TYPE_PICK and key in attributes:
            result_obj[key] = value
    return result_obj


def filter_list(obj_list, attributes, filter_type):
    result_list = []
    for obj in obj_list:
        result_list.append(filter_dict(obj, attributes, filter_type))
    return result_list
