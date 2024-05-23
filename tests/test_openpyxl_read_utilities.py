import unittest
import yaml
import sys

from .context import src


class TestOpenPyxlReadUtilities(unittest.TestCase):

    def setUp(self):
        with open('./tests/test_details.yaml', 'r') as y_file:
            self.test_data_details = yaml.load(y_file, Loader=yaml.FullLoader)
            self.test_file_1_details = self.test_data_details.get('TestOpenPyxlReadUtilities').get('TestExcelFile1')

        self.opu = src.OpenPyxlReadUtilities(excel_file_path=self.test_file_1_details.get('ExcelFilePath'),
                                     worksheet_name=self.test_file_1_details.get('WorksheetName'),
                                     starting_row_number=self.test_file_1_details.get('HeaderRowNumber'),
                                     starting_column_number=self.test_file_1_details.get('StartingColumnNumber'),
                                     )

    def test_init(self):
        self.assertEqual(self.opu.worksheet_name,self.test_file_1_details.get('WorksheetName'))
        self.assertEqual(self.opu.starting_row_number,self.test_file_1_details.get('HeaderRowNumber'))
        self.assertEqual(self.opu.starting_column_number,self.test_file_1_details.get('StartingColumnNumber'))

    def test_read_across_row_until_consecutive_empty_cells(self):

        row_number = 5
        expected_empty_cell_count = 1
        expected_row_length = 7
        self.opu.number_of_consecutive_empty_cells_to_determine_row_ends = expected_empty_cell_count
        self.opu.max_column_number = None
        test_results = self.opu.read_across_row_until_consecutive_empty_cells(row_number=row_number)
        self.assertIsNotNone(test_results)
        self.assertEqual(len(test_results), expected_row_length)
        for i in range(1, expected_empty_cell_count + 1):
            self.assertIsNone(test_results[-i])
        self.assertIsNotNone(test_results[-1 * (expected_empty_cell_count + 1)])

        row_number = 20
        expected_empty_cell_count = 10
        expected_row_length = 10
        self.opu.number_of_consecutive_empty_cells_to_determine_row_ends = expected_empty_cell_count
        self.opu.max_column_number = None
        test_results = self.opu.read_across_row_until_consecutive_empty_cells(row_number=row_number)
        self.assertIsNotNone(test_results)
        self.assertEqual(len(test_results),expected_row_length)
        for i in range(1, expected_empty_cell_count + 1):
            self.assertIsNone(test_results[-i])

        row_number = 157
        expected_empty_cell_count = 2
        expected_row_length = 9
        self.opu.number_of_consecutive_empty_cells_to_determine_row_ends = expected_empty_cell_count
        self.opu.max_column_number = None
        test_results = self.opu.read_across_row_until_consecutive_empty_cells(row_number=row_number)
        self.assertIsNotNone(test_results)
        self.assertEqual(len(test_results),expected_row_length)
        for i in range(1, expected_empty_cell_count + 1):
            self.assertIsNone(test_results[-i])
        self.assertIsNotNone(test_results[-1 * (expected_empty_cell_count + 1)])

        row_number = 205
        expected_empty_cell_count = 0
        expected_row_length = 3
        self.opu.number_of_consecutive_empty_cells_to_determine_row_ends = None
        self.opu.max_column_number = expected_row_length
        test_results = self.opu.read_across_row_until_consecutive_empty_cells(row_number=row_number)
        self.assertIsNotNone(test_results)
        self.assertEqual(len(test_results),expected_row_length)
        for i in range(0, expected_row_length):
            self.assertIsNotNone(test_results[i])

        row_number = 219
        expected_empty_cell_count = 3
        expected_row_length = 17
        self.opu.number_of_consecutive_empty_cells_to_determine_row_ends = None
        self.opu.max_column_number = expected_row_length
        test_results = self.opu.read_across_row_until_consecutive_empty_cells(row_number=row_number)
        self.assertIsNotNone(test_results)
        self.assertEqual(len(test_results),expected_row_length)
        for i in range(1, expected_empty_cell_count + 1):
            self.assertIsNone(test_results[-i])
        self.assertIsNotNone(test_results[-1 * (expected_empty_cell_count + 1)])

    def test_read_rows_until_consecutive_empty_rows(self):
        expected_empty_row_count = 1
        expected_row_count = 10
        self.opu.number_of_consecutive_empty_rows_to_determine_data_ends = expected_empty_row_count
        self.opu.max_row_number = None
        test_results = self.opu.read_rows_until_consecutive_empty_rows()
        self.assertIsNotNone(test_results)
        self.assertEqual(len(test_results),expected_row_count)
        for i in range(1, expected_empty_row_count + 1):
            for j in range(0, expected_empty_row_count):
                self.assertIsNone(test_results[-i][j])

        expected_empty_row_count = 2
        expected_row_count = 21
        self.opu.number_of_consecutive_empty_rows_to_determine_data_ends = expected_empty_row_count
        self.opu.max_row_number = None
        test_results = self.opu.read_rows_until_consecutive_empty_rows()
        self.assertIsNotNone(test_results)
        self.assertEqual( len(test_results),expected_row_count)
        for i in range(1, expected_empty_row_count + 1):
            for j in range(0, expected_empty_row_count):
                self.assertIsNone(test_results[-i][j])

        expected_empty_row_count = 3
        expected_row_count = 32
        self.opu.number_of_consecutive_empty_rows_to_determine_data_ends = expected_empty_row_count
        self.opu.max_row_number = None
        test_results = self.opu.read_rows_until_consecutive_empty_rows()
        self.assertIsNotNone(test_results)
        self.assertEqual(len(test_results),expected_row_count)
        for i in range(1, expected_empty_row_count + 1):
            for j in range(0, expected_empty_row_count):
                self.assertIsNone(test_results[-i][j])

        expected_empty_row_count = 10
        expected_row_count = 109
        self.opu.number_of_consecutive_empty_rows_to_determine_data_ends = None
        self.opu.max_row_number = expected_row_count
        test_results = self.opu.read_rows_until_consecutive_empty_rows()
        self.assertIsNotNone(test_results)
        self.assertEqual(len(test_results),expected_row_count)
        for i in range(1, expected_empty_row_count + 1):
            self.assertEqual([], [x for x in test_results[-i] if x is not None])
        self.assertNotEqual([], [x for x in test_results[-1 * (expected_empty_row_count + 1)] if x is not None])

    def test_get_worksheet_data_as_list_of_lists(self):

        expected_cell_count = 5
        expected_row_count = 5
        self.opu.max_column_number = expected_cell_count
        self.opu.number_of_consecutive_empty_cells_to_determine_row_ends = None
        self.opu.max_row_number = expected_row_count
        self.opu.number_of_consecutive_empty_rows_to_determine_data_ends = None
        test_results = self.opu.get_worksheet_data_as_list_of_lists()
        self.assertIsNotNone(test_results)
        self.assertEqual(len(test_results),expected_row_count)
        for row in test_results:
            self.assertEqual(expected_cell_count, len(row))

    def test_get_worksheet_data_as_dict_list(self):

        expected_cell_count = 5
        expected_row_count = 4
        self.opu.max_column_number = expected_cell_count
        self.opu.number_of_consecutive_empty_cells_to_determine_row_ends = None
        self.opu.max_row_number = expected_row_count+1
        self.opu.number_of_consecutive_empty_rows_to_determine_data_ends = None
        test_results = self.opu.get_worksheet_data_as_dict_list()
        self.assertIsNotNone(test_results)
        self.assertEqual(len(test_results),expected_row_count)
        for row in test_results:
            self.assertEqual(expected_cell_count, len(row))


if __name__ == '__main__':
    unittest.main()
