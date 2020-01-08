Ansible Filter Hetzner
============
... 

Installing
----------

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):

    pip install -U ansible-filter-hetzner


A Simple Example
----------------

Here's how you could use.

    >>> from ansible_filter_hetzner import change_set
    >>> obj_arr = [{"ansible": "filter"}]
    >>> change_set.array_to_dict(obj_arr, "ansible")
    {'filter': {'ansible': 'filter'}}


Links
-----

*   Website: https://newsletter2go.com/
*   License: [MIT](https://github.com/nl2go/ansible-filter-hetzner/blob/master/LICENSE.md)
*   Releases: https://pypi.org/project/ansible-filter-hetzner/
*   Code: https://github.com/nl2go/ansible-filter-hetzner
*   Issue tracker: https://github.com/nl2go/ansible-filter-hetzner/issues

