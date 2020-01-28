#!/usr/bin/python


def get_custom_interface_name_or_default(
        hostname, hostvars, interface_name=None
):
    if interface_name:
        return interface_name

    return get_default_interface_name(hostname, hostvars)


def get_interface_address(hostname, hostvars, interface_name):
    interface = hostvars.get(hostname, {}).get('ansible_' + interface_name)
    if interface:
        return interface.get('ipv4', {}).get('address')

    raise Exception('Interface "{}" is not found for host "{}".'
                    .format(interface_name, hostname))


def get_default_interface_name(hostname, hostvars):
    return hostvars.get(hostname, {})\
        .get('ansible_default_ipv4', {})\
        .get('interface')


def get_point_to_point_connections(
        remote_hostnames, hostname, hostvars, interface_name=None
):
    host_interface_name = get_custom_interface_name_or_default(
        hostname,
        hostvars,
        interface_name
    )
    host_interface_address = get_interface_address(
        hostname,
        hostvars,
        host_interface_name
    )

    connections = []

    for remote_hostname in remote_hostnames:
        if hostname == remote_hostname:
            continue

        remote_host_interface_name = get_custom_interface_name_or_default(
            remote_hostname,
            hostvars,
            interface_name
        )
        remote_host_interface_address = get_interface_address(
            remote_hostname,
            hostvars,
            remote_host_interface_name
        )

        connections.append({
            'local': {
                'hostname': hostname,
                'interface': host_interface_name,
                'address': host_interface_address
            },
            'remote': {
                'hostname': remote_hostname,
                'interface': remote_host_interface_name,
                'address': remote_host_interface_address
            }
        })

    return connections

