import unittest

from ansible_filter_hetzner.omit import *


class OmitTest(unittest.TestCase):

    def test_omit(self):
        obj = [{'foo': 'a', 'bar': 'b'}]
        expected_obj = [{'foo': 'a'}]

        actual_obj = omit(obj, ['bar'])

        self.assertEqual(actual_obj, expected_obj)
