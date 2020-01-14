#!/usr/bin/python


def vswitch_list(host_vars, hosts, attr='hetzner_vswitch_host'):
    results = {}

    for host in hosts:
        host_config = host_vars.get(host)
        vswitch_configs = host_config.get(attr)
        if vswitch_configs:
            verify_is_list(vswitch_configs, 'hetzner_vswitch_host variable must be a list.')
            server_ip = get_default_ip_address(host_config)

            for vswitch_config in vswitch_configs:
                vswitch_name = vswitch_config.get('name')
                vswitch_state = vswitch_config.get('state', 'present')
                result = results.get(vswitch_name)
                if not result:
                    result = {
                        'name': vswitch_name,
                        'server': []
                    }
                    results[vswitch_name] = result

                result.get('server').append({
                    'server_ip': server_ip,
                    'state': vswitch_state
                })

    return list(results.values())


def get_default_ip_address(host_config):
    ansible_host = host_config.get('ansible_host')
    if ansible_host:
        return ansible_host

    return host_config.get('ansible_default_ipv4').get('address')


def verify_is_list(value, msg):
    if not isinstance(value, list):
        raise TypeError(msg)
