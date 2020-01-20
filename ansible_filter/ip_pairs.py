#!/usr/bin/python


def unique_ip_pairs(hostname_list, ansible_host, hostvars, network_interfaces=None):
    if not network_interfaces:
        network_interfaces = {}

    results = []

    for hostname in hostname_list:
        remote_ansible_host = hostvars[hostname].get("ansible_host")

        if ansible_host == remote_ansible_host:
            continue

        results.append({
            "target_hostname": hostname,
            "first_ip": ansible_host,
            "second_ip": remote_ansible_host
        })

        remote_network_interfaces = hostvars[hostname].get("network_interfaces", {})
        remote_ip_pairs = get_ip_pairs(hostname, ansible_host, remote_network_interfaces, "target_interface")
        source_ip_pairs = get_ip_pairs(hostname, remote_ansible_host, network_interfaces, "source_interface")

        results = results + remote_ip_pairs + source_ip_pairs

    return results


def get_ip_pairs(hostname, host, network_interfaces, interface_type):
    ip_pairs = []

    for interface_name, interface in network_interfaces.items():
        interface_ip = interface.get("ipaddress")
        if not interface_ip:
            continue

        first_ip = interface_ip if interface_type == "source_interface" else host
        second_ip = host if interface_type == "source_interface" else interface_ip
        ip_pair = {
            "target_hostname": hostname,
            interface_type: interface_name,
            "first_ip": first_ip,
            "second_ip": second_ip
        }
        ip_pairs.append(ip_pair)

    return ip_pairs
