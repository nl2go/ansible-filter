import unittest

from ansible_filter.omit import *


class OmitTest(unittest.TestCase):

    def test_omit_with_list(self):
        obj = [{'foo': 'a', 'bar': 'b'}]
        expected_obj = [{'foo': 'a'}]

        actual_obj = omit(obj, ['bar'])

        self.assertEqual(actual_obj, expected_obj)

    def test_omit_with_dict(self):
        obj = {'foo': 'a', 'bar': 'b'}
        expected_obj = {'foo': 'a'}

        actual_obj = omit(obj, ['bar'])

        self.assertEqual(actual_obj, expected_obj)

    def test_omit_with_not_supported_type(self):
        with self.assertRaises(TypeError) as context:
            omit("someString", ['bar'])

        self.assertTrue('Given object is neither a dictionary nor a list.' in str(context.exception))
