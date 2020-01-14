[![Travis (.com) branch](https://img.shields.io/travis/com/nl2go/ansible-filter-hetzner/master)](https://travis-ci.com/nl2go/ansible-filter-hetzner)
[![Codecov](https://img.shields.io/codecov/c/github/nl2go/ansible-filter-hetzner)](https://codecov.io/gh/nl2go/ansible-filter-hetzner)
[![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/nl2go/ansible-filter-hetzner)](https://codeclimate.com/github/nl2go/ansible-filter-hetzner)
[![PyPI](https://img.shields.io/pypi/v/ansible-filter-hetzner)](https://pypi.org/project/ansible-filter-hetzner/#history)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/ansible-filter-hetzner)](https://pypi.org/project/ansible-filter-hetzner/#files)

# Ansible Filter Hetzner

Filter plugin set to interact with the [Hetzer Robot API](https://robot.your-server.de/doc/webservice/en.html) using [Ansible](https://www.ansible.com/).
Following functionality is provided:
- Compute the resource change set between local and origin state.
- URL encode request body
- Filter dictionary by key

## Install

### PyPI

    pip install -U ansible-filter-hetzner

### Source

    git clone git@github.com:nl2go/ansible-filter-hetzner.git
    cd ansible-filter-hetzner/
    pip install .

## Filters

### Change Set
Computes the change set between a list of objects using a key attribute non-recursively.

The filter arguments `local` and `origin` are non-associative. Objects present at the `origin` but missing
within `local` are considered non managed.

The result is a change set with a map of lists to:

- `create` - objects to create at `origin`
- `update` - objects to update at `origin`
- `delete` - objects to delete at `origin`
- `noop` - objects with no operation required

Useful to interact with any kind of a stateful API.


    from ansible_filter_hetzner import change_set
    
    local = [{ 'id': 1, 'foo': 'bar' }, { 'id': 2, 'foo': 'foo' }, { 'id': 3, 'foz':'baz' }, { 'id': 4, 'state': 'absent' }]
    origin = [{ 'id': 2, 'foo': 'bar' }, { 'id': 3, 'foz':'baz' }, { 'id': 4, 'x': 'y' }, { 'id': 5, 'foo': 'bar' }]
    
    result = change_set.change_set(local, origin, 'id')
    print(result)  
    
    [
        'create': [{ 'id': 1, 'foo': 'bar' }],
        'update': [{ 'id': 2, 'foo': 'foo' }],
        'delete': [{ 'id': 4, 'x': 'y' }],
        'noop': [{ 'id': 3, 'foz': 'baz' }],
    ]

### Form URL Encode
Encodes arbitrary objects to form URL format.

    from ansible_filter_hetzner import form_urlencode
    
    obj = { 'foo': 'bar', 'foz': ['baz'] }
    
    result = form_urlencode.form_urlencode(obj)
    print(result)

    foo=bar&foz[0]=baz&

### Pick
Filters a list of objects retaining attributes only matching the names passed as argument, non-recursively.

    from ansible_filter_hetzner import pick
    
    elements = [{ 'foo': 'bar', 'foz': 'baz' }]
    
    result = pick.pick(elements, ['foo'])
    print(result)

    [{ 'foo': 'bar' }]
    
### Omit
Filters a list objects omitting attributes matching the names passed as argument, non-recursively.    

    from ansible_filter_hetzner import omit
    
    elements = [{ 'foo': 'bar', 'foz': 'baz' }]
    
    result = omit.omit(elements, ['foo'])
    print(result)

    [{ 'foz': 'baz' }]

### Group By
Groups elements by key attribute.

    from ansible_filter_hetzner import group_by
    
    left = [{ 'id': '1', 'foo': 'a' }, { 'id': '2', 'foz': 'x' }]
    right = [{ 'id': '1', 'foo': 'b' }, { 'id': '2', 'foz': 'y' }]
    
    result = group_by.group_by(left, right, 'id')
    print(result)

    [
        { 'id': '1', 'group': [{ 'id': '1', 'foo': 'a' }, { 'id': '1', 'foo': 'b' }] }, 
        { 'id': '2', 'group': [{ 'id': '2', 'foz': 'x' }, { 'id': '2', 'foz': 'y' }] }
    ]

### List 2 Dict
Converts a list to dict by key attribute.

    from ansible_filter_hetzner import list_to_dict
    
    elements = [{ 'id': '1', 'foo': 'bar' }, { 'id': '2', 'foz': 'baz' }]
    
    result = list_to_dict.list_to_dict(elements, 'id')
    print(result)
    
    {'1': {'foo': 'bar', 'id': '1'}, '2': {'id': '2', 'foz': 'baz'}}

## Links

*   Website: https://newsletter2go.com/
*   License: [MIT](https://github.com/nl2go/ansible-filter-hetzner/blob/master/LICENSE.md)
*   Releases: https://pypi.org/project/ansible-filter-hetzner/
*   Code: https://github.com/nl2go/ansible-filter-hetzner
*   Issue tracker: https://github.com/nl2go/ansible-filter-hetzner/issues

