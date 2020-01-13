# Ansible Filter Hetzner
[![Travis (.com) branch](https://img.shields.io/travis/com/nl2go/ansible-filter-hetzner/master)](https://travis-ci.com/nl2go/ansible-filter-hetzner)
[![Codecov](https://img.shields.io/codecov/c/github/nl2go/ansible-filter-hetzner)](https://codecov.io/gh/nl2go/ansible-filter-hetzner)
![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/nl2go/ansible-filter-hetzner)
[![PyPI](https://img.shields.io/pypi/v/ansible-filter-hetzner)](https://pypi.org/project/ansible-filter-hetzner/#history)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/ansible-filter-hetzner)](https://pypi.org/project/ansible-filter-hetzner/#files)


... 

## Installing

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):

    pip install -U ansible-filter-hetzner


Install from source:

    git clone git@github.com:nl2go/ansible-filter-hetzner.git
    cd ansible-filter-hetzner/
    pip install .


## A Simple Example

Here's how you could use.

    >>> from ansible_filter_hetzner import change_set
    >>> obj_arr = [{"ansible": "filter"}]
    >>> change_set.array_to_dict(obj_arr, "ansible")
    {'filter': {'ansible': 'filter'}}


## Links

*   Website: https://newsletter2go.com/
*   License: [MIT](https://github.com/nl2go/ansible-filter-hetzner/blob/master/LICENSE.md)
*   Releases: https://pypi.org/project/ansible-filter-hetzner/
*   Code: https://github.com/nl2go/ansible-filter-hetzner
*   Issue tracker: https://github.com/nl2go/ansible-filter-hetzner/issues

