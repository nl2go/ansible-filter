import unittest

from ansible_filter import list_to_dict


class ListToDictTest(unittest.TestCase):

    def test_list_to_dict(self):
        list1 = [{'name': 'foo', 'x': 'y'}, {'name': 'bar', 'a': 'b'}]
        expected_result = {'foo': {'name': 'foo', 'x': 'y'}, 'bar': {'name': 'bar', 'a': 'b'}}

        actual_result = list_to_dict(list1, 'name')

        self.assertEqual(actual_result, expected_result)
