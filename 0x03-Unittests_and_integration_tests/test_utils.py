#!/usr/bin/env python3
"""Parameterize a unit test"""
import unittest
from unittest.mock import patch, Mock
from typing import Dict, Tuple, Union
from parameterized import parameterized
from utils import (
    access_nested_map,
    get_json,
    memoize,
)


class TestAccessNestedMap(unittest.TestCase):
    """
    TestAccessNestedMap class that inherits
    from unittest.TestCase.Implement the TestAccessNestedMap.
    test_access_nested_map method to test that the method
    returns what it is supposed to.
    Decorate the method with @parameterized.expand to test
    the function for following inputs:
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map: Dict,
                               path: Tuple,
                               expected: Union[Dict, int]) -> None:
        """a method that test and return the expected result"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a"), KeyError),
        ({"a": 1}, ("a", "b"), KeyError)
    ])
    def test_access_nested_map_exception(self, nested_map: Dict,
                                         path: Tuple, expected: Exception):
        """test that raises key error exceptions"""
        with self.assertRaises(expected):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Testing api calls Mock HTTP calls"""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str,
                      test_payload: Dict,) -> None:
        """ Mocking the json method of the mock object"""
        thekwags = {'json.return_value': test_payload}
        with patch("requests.get", return_value=Mock(**thekwags)) as req_get:
            self.assertEqual(get_json(test_url), test_payload)
            req_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Tests the memoize function."""
    def test_memoize(self) -> None:
        """Tests memoize's output."""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()
        with patch.object(
                TestClass,
                "a_method",
                return_value=lambda: 42,
                ) as memo_func:
            test_class = TestClass()
            self.assertEqual(test_class.a_property(), 42)
            self.assertEqual(test_class.a_property(), 42)
            memo_func.assert_called_once()


if __name__ == '__main__':
    unittest.main()
