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
        remote_ip_pairs = get_ip_pairs_from_remote_network_interfaces(hostname, ansible_host, remote_network_interfaces)
        source_ip_pairs = get_ip_pairs_from_network_interfaces(hostname, remote_ansible_host, network_interfaces)

        results = results + remote_ip_pairs + source_ip_pairs

    return results


def get_ip_pairs_from_remote_network_interfaces(hostname, ansible_host, remote_network_interfaces):
    ip_pairs = []

    for interface_name, interface in remote_network_interfaces.items():
        interface_ip = interface.get("ipaddress")
        if not interface_ip:
            continue

        ip_pairs.append({
            "target_hostname": hostname,
            "target_interface": interface_name,
            "first_ip": ansible_host,
            "second_ip": interface_ip
        })

    return ip_pairs


def get_ip_pairs_from_network_interfaces(hostname, remote_ansible_host, network_interfaces):
    ip_pairs = []

    for interface_name, interface in network_interfaces.items():
        interface_ip = interface.get("ipaddress")
        if not interface_ip:
            continue

        ip_pairs.append({
            "target_hostname": hostname,
            "source_interface": interface_name,
            "first_ip": interface_ip,
            "second_ip": remote_ansible_host
        })

    return ip_pairs
