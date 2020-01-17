import sys
import unittest

from ansible_filter.ipsec import unique_ip_pairs, get_ip_pairs_by_hostname


class IpsecTest(unittest.TestCase):
    def test_unique_ip_pairs_with_equal_host(self):
        hostname = "hostname"
        ansible_host = "ansible_host"
        network_interfaces = None

        hostname_list = [hostname]
        hostvars = {
            hostname: {
                "ansible_host": ansible_host,
            }
        }

        expected = []

        actual = unique_ip_pairs(hostname_list, ansible_host, hostvars, network_interfaces)

        self.assertListEqual(expected, actual)

    def test_unique_ip_pairs_with_network_interfaces(self):
        first_source_interface = {
            "ipaddress": "127.0.0.1"
        }
        second_source_interface = {}

        hostname = "hostname"
        ansible_host = "ansible_host"
        remote_ansible_host = "remote_ansible_host"
        network_interfaces = {
            "first_source_interface": first_source_interface,
            "second_source_interface": second_source_interface
        }

        hostname_list = [hostname]
        hostvars = {
            hostname: {
                "ansible_host": remote_ansible_host,
            }
        }

        expected = [
            {
                "target_hostname": hostname,
                "first_ip": ansible_host,
                "second_ip": remote_ansible_host
            },
            {
                "target_hostname": hostname,
                "source_interface": "first_source_interface",
                "first_ip": "127.0.0.1",
                "second_ip": remote_ansible_host
            }
        ]

        actual = unique_ip_pairs(hostname_list, ansible_host, hostvars, network_interfaces)

        if sys.version_info.major == 2:
            self.assertItemsEqual(expected, actual)
        else:
            self.assertListEqual(expected, actual)

    def test_unique_ip_pairs_without_network_interfaces(self):
        first_remote_interface = {
            "ipaddress": "127.0.0.1"
        }
        second_remote_interface = {}

        hostname = "hostname"
        ansible_host = "ansible_host"
        remote_ansible_host = "remote_ansible_host"
        remote_network_interfaces = {
            "first_remote_interface": first_remote_interface,
            "second_remote_interface": second_remote_interface
        }
        network_interfaces = None

        hostname_list = [hostname]
        hostvars = {
            hostname: {
                "ansible_host": remote_ansible_host,
                "network_interfaces": remote_network_interfaces
            }
        }

        expected = [
            {
                "target_hostname": hostname,
                "first_ip": ansible_host,
                "second_ip": remote_ansible_host
            },
            {
                "target_hostname": hostname,
                "target_interface": "first_remote_interface",
                "first_ip": ansible_host,
                "second_ip": "127.0.0.1"
            }
        ]

        actual = unique_ip_pairs(hostname_list, ansible_host, hostvars, network_interfaces)

        if sys.version_info.major == 2:
            self.assertItemsEqual(expected, actual)
        else:
            self.assertListEqual(expected, actual)
