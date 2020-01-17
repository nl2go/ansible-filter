import sys
import unittest

import copy

from ansible_filter.change_set import (
    ACTION_CREATE,
    ACTION_UPDATE,
    ACTION_DELETE,
    ACTION_NOOP,
    change_set,
    is_all_list,
    is_equal_list,
    is_equal_bool,
    dict_to_array,
    str2bool
)


class ChangeSetTest(unittest.TestCase):
    default_change_set = {
        'create': [],
        'update': [],
        'delete': [],
        'noop': []
    }

    def test_set_action_create(self):
        local = [{'foo': 'bar', 'name': 'obj1'}]
        origin = []
        expected_change_set = copy.deepcopy(self.default_change_set)
        expected_change_set.update({
            'create': [{'foo': 'bar', 'name': 'obj1'}],
        })

        actual_change_set = change_set(local, origin)

        self.assertEqual(actual_change_set, expected_change_set)

    def test_set_action_create_if_state_present(self):
        local = [{'foo': 'bar', 'name': 'obj1', 'state': 'present'}]
        origin = []
        expected_change_set = copy.deepcopy(self.default_change_set)
        expected_change_set.update({
            'create': [{'foo': 'bar', 'name': 'obj1'}]
        })

        actual_change_set = change_set(local, origin)

        self.assertEqual(actual_change_set, expected_change_set)

    def test_set_action_noop_if_state_absent_no_origin(self):
        local = [{'foo': 'bar', 'name': 'obj1', 'state': 'absent'}]
        origin = []
        expected_change_set = copy.deepcopy(self.default_change_set)
        expected_change_set.update({

            'noop': [{'foo': 'bar', 'name': 'obj1'}]
        })

        actual_change_set = change_set(local, origin)

        self.assertEqual(actual_change_set, expected_change_set)

    def test_set_action_delete_if_state_absent(self):
        local = [{'foo': 'bar', 'name': 'obj1', 'state': 'absent'}]
        origin = [{'foo': 'bar', 'id': 1, 'name': 'obj1'}]
        expected_change_set = copy.deepcopy(self.default_change_set)
        expected_change_set.update({
            'delete': [{'foo': 'bar', 'id': 1, 'name': 'obj1'}]
        })

        actual_change_set = change_set(local, origin)

        self.assertEqual(actual_change_set, expected_change_set)

    def test_set_action_update(self):
        local = [{'foo': 'baz', 'name': 'obj1'}]
        origin = [{'foo': 'bar', 'id': 1, 'name': 'obj1'}]
        expected_change_set = copy.deepcopy(self.default_change_set)
        expected_change_set.update({
            'update': [{'foo': 'baz', 'id': 1, 'name': 'obj1'}]
        })

        actual_change_set = change_set(local, origin)

        self.assertEqual(actual_change_set, expected_change_set)

    def test_set_action_noop_if_true_bool_str(self):
        local = [{'foo': 'true', 'name': 'obj1'}]
        origin = [{'foo': True, 'id': 1, 'name': 'obj1'}]
        expected_change_set = copy.deepcopy(self.default_change_set)
        expected_change_set.update({
            'noop': [{'foo': 'true', 'id': 1, 'name': 'obj1'}]
        })

        actual_change_set = change_set(local, origin)

        self.assertEqual(actual_change_set, expected_change_set)

    def test_set_action_noop_if_false_bool_str(self):
        local = [{'foo': 'false', 'name': 'obj1'}]
        origin = [{'foo': False, 'id': 1, 'name': 'obj1'}]
        expected_change_set = copy.deepcopy(self.default_change_set)
        expected_change_set.update({
            'noop': [{'foo': 'false', 'id': 1, 'name': 'obj1'}]
        })

        actual_change_set = change_set(local, origin)

        self.assertEqual(actual_change_set, expected_change_set)

    def test_set_action_noop_if_field_empty_dict_or_list(self):
        local = [{'empty': [], 'foo': 'true', 'name': 'obj1'}]
        origin = [{'empty': {}, 'foo': True, 'id': 1, 'name': 'obj1'}]
        expected_change_set = copy.deepcopy(self.default_change_set)
        expected_change_set.update({
            'noop': [{'empty': [], 'foo': 'true', 'id': 1, 'name': 'obj1'}]
        })

        actual_change_set = change_set(local, origin)

        self.assertEqual(actual_change_set, expected_change_set)

    def test_set_action_noop(self):
        local = [{'foo': 'bar', 'name': 'obj1'}]
        origin = [{'foo': 'bar', 'id': 1, 'name': 'obj1'}]
        expected_change_set = copy.deepcopy(self.default_change_set)
        expected_change_set.update({
            'noop': [{'foo': 'bar', 'id': 1, 'name': 'obj1'}]
        })

        actual_change_set = change_set(local, origin)

        self.assertEqual(actual_change_set, expected_change_set)

    def test_set_action_noop_if_state_present(self):
        local = [{'foo': 'bar', 'name': 'obj2', 'state': 'present'}]
        origin = [{'foo': 'bar', 'id': 1, 'name': 'obj2'}]
        expected_change_set = copy.deepcopy(self.default_change_set)
        expected_change_set.update({
            'noop': [{'foo': 'bar', 'id': 1, 'name': 'obj2'}]
        })

        actual_change_set = change_set(local, origin)

        self.assertEqual(actual_change_set, expected_change_set)

    def test_set_action_noop_if_origin_nested_object_has_additional_properties(self):
        local = [{'foo': 'bar', 'name': 'obj2', 'items': [{'foo': 'bar'}]}]
        origin = [{'foo': 'bar', 'name': 'obj2', 'items': [{'foo': 'bar', 'foz': 'baz'}]}]
        expected_change_set = copy.deepcopy(self.default_change_set)
        expected_change_set.update({
            'noop': [{'foo': 'bar', 'name': 'obj2', 'items': [{'foo': 'bar'}]}]
        })

        actual_change_set = change_set(local, origin)

        self.assertEqual(actual_change_set, expected_change_set)

    def test_set_action_noop_if_local_and_origin_dict(self):
        local = {'foo': 'bar', 'name': 'obj2'}
        origin = {'foo': 'bar', 'name': 'obj2'}
        expected_change_set = copy.deepcopy(self.default_change_set)
        expected_change_set.update({
            'noop': [{'foo': 'bar', 'name': 'obj2'}]
        })

        actual_change_set = change_set(local, origin)

        self.assertEqual(actual_change_set, expected_change_set)

    def test_set_action_noop_if_local_is_none(self):
        expected_change_set = {
            ACTION_CREATE: [],
            ACTION_UPDATE: [],
            ACTION_DELETE: [],
            ACTION_NOOP: []
        }

        actual_change_set = change_set(None, None)

        self.assertEqual(actual_change_set, expected_change_set)

    def test_set_action_noop_if_local_is_neither_dict_nor_list(self):
        with self.assertRaises(TypeError) as context:
            change_set("someString", ['bar'])

    def test_is_all_list(self):
        left = ["left"]
        right = ["right"]

        actual = is_all_list(left, right)

        self.assertTrue(actual)

    def test_is_equal_list(self):
        left = ["same"]
        right = ["same"]

        actual = is_equal_list(left, right)

        self.assertTrue(actual)

    def test_is_equal_list_with_different_params(self):
        left = ["one"]
        right = ["two"]

        actual = is_equal_list(left, right)

        self.assertFalse(actual)

    def test_is_equal_bool(self):
        left = True
        right = True

        actual = is_equal_bool(left, right)

        self.assertTrue(actual)

    def test_is_equal_bool_with_string_bool(self):
        left = "true"
        right = "false"

        actual = is_equal_bool(left, right)

        self.assertFalse(actual)

    def test_dict_to_array(self):
        obj = {"first": "Hello", "second": "How are you?"}
        expected = ["Hello", "How are you?"]

        actual = dict_to_array(obj)

        if sys.version_info.major == 2:
            self.assertItemsEqual(expected, actual)
        else:
            self.assertListEqual(expected, actual)

    def test_str2bool(self):
        v = "true"

        actual = str2bool(v)

        self.assertTrue(actual)
