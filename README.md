[![Travis (.com) branch](https://img.shields.io/travis/com/nl2go/ansible-filter/master)](https://travis-ci.com/nl2go/ansible-filter)
[![Codecov](https://img.shields.io/codecov/c/github/nl2go/ansible-filter)](https://codecov.io/gh/nl2go/ansible-filter)
[![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/nl2go/ansible-filter)](https://codeclimate.com/github/nl2go/ansible-filter)
[![PyPI](https://img.shields.io/pypi/v/ansible-filter)](https://pypi.org/project/ansible-filter/#history)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/ansible-filter)](https://pypi.org/project/ansible-filter/#files)

# Ansible Filter

Contains [Ansible](https://www.ansible.com/) related filter set for collection/object operations. Aims to extend the official
[Ansible Filters](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html).

Available filters are listed [below](#filters).

## Install

### PyPI

    pip install -U ansible-filter

### Source

    git clone git@github.com:nl2go/ansible-filter.git
    cd ansible-filter/
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


    from ansible_filter import change_set
    
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

    from ansible_filter import form_urlencode
    
    obj = { 'foo': 'bar', 'foz': ['baz'] }
    
    result = form_urlencode.form_urlencode(obj)
    print(result)

    foo=bar&foz[0]=baz&

### Pick
Filters a list of objects retaining attributes only matching the names passed as argument, non-recursively.

    from ansible_filter import pick
    
    elements = [{ 'foo': 'bar', 'foz': 'baz' }]
    
    result = pick.pick(elements, ['foo'])
    print(result)

    [{ 'foo': 'bar' }]
    
### Omit
Filters a list objects omitting attributes matching the names passed as argument, non-recursively.    

    from ansible_filter import omit
    
    elements = [{ 'foo': 'bar', 'foz': 'baz' }]
    
    result = omit.omit(elements, ['foo'])
    print(result)

    [{ 'foz': 'baz' }]

### Group By
Groups elements by key attribute.

    from ansible_filter import group_by
    
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

    from ansible_filter import list_to_dict
    
    elements = [{ 'id': '1', 'foo': 'bar' }, { 'id': '2', 'foz': 'baz' }]
    
    result = list_to_dict.list_to_dict(elements, 'id')
    print(result)
    
    {'1': {'foo': 'bar', 'id': '1'}, '2': {'id': '2', 'foz': 'baz'}}

### Point to Point Connections
Resolves point to point connections between the local and remote hosts.

    from ansible_filter import network
    
    remote_hostnames = ['two', 'three']
    hostname = 'one'
    hostvars = {
        'one': {
            'ansible_default_ipv4': {
                'interface': 'eth0'
            },
            'ansible_eth0': {
                'ipv4': {
                    'address': '127.0.0.1',
                }
            }
        },
        'two': {
            'ansible_default_ipv4': {
                'interface': 'eth0'
            },
            'ansible_eth0': {
                'ipv4': {
                    'address': '127.0.0.2',
                }
            }
        },
        'three': {
            'ansible_default_ipv4': {
                'interface': 'eth0'
            },
            'ansible_eth0': {
                'ipv4': {
                    'address': '127.0.0.3',
                }
            }        
        }
    }
    
    result = network.get_point_to_point_connections(remote_hostnames, hostname, hostvars)

    [
      {
        'remote': {
          'interface': 'eth0',
          'hostname': 'two',
          'address': '127.0.0.2'
        },
        'local': {
          'interface': 'eth0',
          'hostname': 'one',
          'address': '127.0.0.1'
        }
      },
      {
        'remote': {
          'interface': 'eth0',
          'hostname': 'three',
          'address': '127.0.0.3'
        },
        'local': {
          'interface': 'eth0',
          'hostname': 'one',
          'address': '127.0.0.1'
        }
      }
    ]

## Links

*   Website: https://newsletter2go.com/
*   License: [MIT](https://github.com/nl2go/ansible-filter/blob/master/LICENSE.md)
*   Releases: https://pypi.org/project/ansible-filter/
*   Code: https://github.com/nl2go/ansible-filter
*   Issue tracker: https://github.com/nl2go/ansible-filter/issues

