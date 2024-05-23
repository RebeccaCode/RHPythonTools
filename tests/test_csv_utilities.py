import json
import unittest
import sys
import os

from .context import src


class TestCsvUtilities(unittest.TestCase):

    def setUp(self) -> None:
        print(os.getcwd())
        return super().setUp()

    def test_write_json_from_dict_list_each_element_single_line(self):
        simple_dict = [{'a': 'a1', 'b': 'b1', 'c': 'c1'},
                       {'a': 'a2', 'b': 'b2', 'c': 'c2'},
                       {'a': 'a3', 'b': 'b3', 'c': 'c3'}
                       ]

        simple_dict_output_path = './tests/test_result_files/simple_dict_output.json'
        src.CsvUtilities.write_json_from_dict_list_each_element_single_line(the_dict=simple_dict,
                                                                          file_path=simple_dict_output_path)

        self.assertTrue(os.path.isfile(simple_dict_output_path))
        test_result_stats = os.stat(simple_dict_output_path)
        self.assertIsNotNone(test_result_stats)
        self.assertIsNotNone(test_result_stats.st_size)
        self.assertGreater(test_result_stats.st_size, 0)

    def test_write_json_from_dict_multiple_lines(self):
        nested_dict = [{"EPC Discovery Details": {"Attribute Name": "Cable Service Switchers - Top 10% - Highly Likely",
                                                  "Attribute Size": 24291570,
                                                  "Attribute Path List": ["Epsilon", "Market Trends",
                                                                          "Adhoc Custom Audiences"],
                                                  "Attribute Path String": "Epsilon < Market Trends < Adhoc Custom Audiences"},
                        "Taxonomy": {"Categorization": {"Friendly Name": "Cable Service", "Categories": ["Switcher"]},
                                     "Never Use": False}},
                       {"EPC Discovery Details": {
                           "Attribute Name": "Internet Service Switchers - Top 10% - Highly Likely",
                           "Attribute Size": 20767312,
                           "Attribute Path List": ["Epsilon", "Market Trends", "Adhoc Custom Audiences"],
                           "Attribute Path String": "Epsilon < Market Trends < Adhoc Custom Audiences"}, "Taxonomy": {
                           "Categorization": {"Friendly Name": "Internet Service", "Categories": ["Switcher"]},
                           "Never Use": False}},
                       {"EPC Discovery Details": {
                           "Attribute Name": "Mobile Phone Service Switchers - Top 10% - Highly Likely",
                           "Attribute Size": 29599568,
                           "Attribute Path List": ["Epsilon", "Market Trends", "Adhoc Custom Audiences"],
                           "Attribute Path String": "Epsilon < Market Trends < Adhoc Custom Audiences"}, "Taxonomy": {
                           "Categorization": {"Friendly Name": "Mobile Phone Service", "Categories": ["Switcher"]},
                           "Never Use": False}},
                       ]

        nested_dict_output_path = './tests/test_result_files/nested_dict_output.json'
        src.CsvUtilities.write_json_from_dict_multiple_lines(the_dict=nested_dict, file_path=nested_dict_output_path)

        self.assertTrue(os.path.isfile(nested_dict_output_path))
        test_result_stats = os.stat(nested_dict_output_path)
        self.assertIsNotNone(test_result_stats)
        self.assertIsNotNone(test_result_stats.st_size)
        self.assertGreater(test_result_stats.st_size, 0)

        json_data = json.dumps(nested_dict, default=lambda o: o.__dict__, indent=4)

if __name__ == '__main__':
    unittest.main()
