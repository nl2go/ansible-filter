import unittest

from ansible_filter.network_encryption import *


class NetworkEncryptionTest(unittest.TestCase):
    def test_single(self):
        local_hostname = "local_hostname"
        remote_hostname = local_hostname
        interface_name = "interface_name"
        remote_hostnames = [remote_hostname]
        hostvars = {
            remote_hostname: {
                "ansible_" + interface_name: {
                    "ipv4": {
                        "address": "first_address"
                    }
                }
            }
        }

        expected = []
        actual = get_point_to_point_connections(
            remote_hostnames,
            local_hostname,
            hostvars,
            interface_name
        )

        self.assertEqual(expected, actual)

    def test_default_interface_name(self):
        local_hostname = "local_hostname"
        remote_hostname = local_hostname
        default_interface_name = "default_interface"
        remote_hostnames = [remote_hostname]
        hostvars = {
            remote_hostname: {
                "ansible_" + default_interface_name: {
                    "ipv4": {
                        "address": "first_address"
                    }
                },
                "ansible_default_ipv4": {
                    "interface": default_interface_name
                }
            }
        }

        expected = []
        actual = get_point_to_point_connections(
            remote_hostnames,
            local_hostname,
            hostvars
        )

        self.assertEqual(expected, actual)

    def test_nonexistent_interface_for_host(self):
        local_hostname = "local_hostname"
        interface_name = "interface_name"
        remote_hostnames = []
        hostvars = {}

        expected = 'Interface "{}" is not found for host "{}".'\
            .format(interface_name, local_hostname)

        with self.assertRaises(Exception) as context:
            get_point_to_point_connections(
                remote_hostnames,
                local_hostname,
                hostvars,
                interface_name
            )
        actual = context.exception

        self.assertIn(expected, actual)

    def test_multiple_host(self):
        local_hostname = "local_hostname"
        remote_hostname = "remote_host"
        local_address = "local_address"
        remote_address = "remote_address"
        interface_name = "interface_name"
        remote_hostnames = [local_hostname, remote_hostname]
        hostvars = {
            local_hostname: {
                "ansible_" + interface_name: {
                    "ipv4": {
                        "address": local_address
                    }
                }
            },
            remote_hostname: {
                "ansible_" + interface_name: {
                    "ipv4": {
                        "address": remote_address
                    }
                }
            }
        }

        expected = [
            {
                "local": {
                    "hostname": local_hostname,
                    "interface": interface_name,
                    "address": local_address
                },
                "remote": {
                    "hostname": remote_hostname,
                    "interface": interface_name,
                    "address": remote_address
                }
            }
        ]

        actual = get_point_to_point_connections(
            remote_hostnames,
            local_hostname,
            hostvars,
            interface_name
        )

        self.assertEqual(expected, actual)
