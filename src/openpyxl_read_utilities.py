from first import first
import openpyxl


class OpenPyxlReadUtilities:
    def __init__(self,
                 excel_file_path,
                 worksheet_name,
                 starting_row_number,
                 starting_column_number,
                 max_column_number=None,
                 number_of_consecutive_empty_cells_to_determine_row_ends=3,
                 max_row_number=None,
                 number_of_consecutive_empty_rows_to_determine_data_ends=3,
                 ):
        """
        :param excel_file_path: Full path of the excel file to read.
        :param worksheet_name: Name of the worksheet to read.
        :param starting_row_number: the number of the row to start reading. Excel uses a 1-based index.
        :param starting_column_number: the ascii number of the column to start reading.
        :param max_column_number: ascii value of the column letter to stop reading at. Use this OR number_of_empty_cells_to_determine_row_ends
        :param number_of_consecutive_empty_cells_to_determine_row_ends: number of consecutive empty cells that determines when to stop reading the row. Use this OR max_column_numbers
        :param max_row_number: ascii value of the row number to stop reading at. Use this OR number_of_rows_to_determine_data_ends
        :param number_of_consecutive_empty_rows_to_determine_data_ends: number of consecutive empty rows that determines when to stop reading the worksheet. Use this OR max_row_number.
        """

        self.excel_file_path = excel_file_path
        self.worksheet_name = worksheet_name
        self.starting_row_number = starting_row_number
        self.starting_column_number = starting_column_number
        self.max_column_number = max_column_number
        self.number_of_consecutive_empty_cells_to_determine_row_ends = number_of_consecutive_empty_cells_to_determine_row_ends
        self.max_row_number = max_row_number
        self.number_of_consecutive_empty_rows_to_determine_data_ends = number_of_consecutive_empty_rows_to_determine_data_ends

        self.workbook = openpyxl.load_workbook(filename=self.excel_file_path)

        if self.worksheet_name not in self.workbook.sheetnames:
            raise Exception(f'Worksheet not found: {self.worksheet_name}')
        self.worksheet = self.workbook[self.worksheet_name]

    def read_across_row_until_consecutive_empty_cells(self, row_number):
        """
        Read data from row, column by column, until there are a specified consecutive number of empty cells in that row

        Most params taken from class initialization parameters.

        :param row_number: row number to read data from; Excel row numbers start at 1.

        :return: list of data from the row
        """
        row_data = []
        continue_reading = True
        column_index = self.starting_column_number
        number_found_consecutive_empty_cells = 0
        last_empty_column_number = 0

        while continue_reading:
            letter = OpenPyxlReadUtilities.__number_to_excel_column_letter__(column_index)
            cell_address = f'{letter}{row_number}'
            cell_data = self.workbook[self.worksheet_name][cell_address].value

            row_data.append(cell_data)

            if not cell_data or cell_data == '':
                if column_index == last_empty_column_number + 1:
                    number_found_consecutive_empty_cells += 1
                else:
                    number_found_consecutive_empty_cells = 1
                last_empty_column_number = column_index

            continue_reading = (self.max_column_number is None or (
                    self.max_column_number > 0 and column_index < self.max_column_number)) and (
                                       self.number_of_consecutive_empty_cells_to_determine_row_ends is None or (
                                       self.number_of_consecutive_empty_cells_to_determine_row_ends > 0 and number_found_consecutive_empty_cells < self.number_of_consecutive_empty_cells_to_determine_row_ends))

            column_index += 1

        # print(row_number)
        # print(row_data)

        return row_data

    def read_rows_until_consecutive_empty_rows(self):
        """
        Read data from row, column by column, until there are a specified consecutive number of empty cells in that row.
        
        All params taken from class initiation parameters.
        
        :return: list of row_data lists.
        """
        worksheet_data = []
        continue_reading = True
        row_index = self.starting_row_number
        number_found_consecutive_empty_rows = 0
        last_empty_row_number = 0

        while continue_reading:
            row_data = self.read_across_row_until_consecutive_empty_cells(row_number=row_index)

            worksheet_data.append(row_data)

            if not first([x for x in row_data if x is not None]):
                if row_index == last_empty_row_number + 1:
                    number_found_consecutive_empty_rows += 1
                else:
                    number_found_consecutive_empty_rows = 1
                last_empty_row_number = row_index

            continue_reading = (self.max_row_number is None or (
                                       self.max_row_number > 0 and row_index < self.max_row_number)) and (
                                       self.number_of_consecutive_empty_rows_to_determine_data_ends is None or (
                                       self.number_of_consecutive_empty_rows_to_determine_data_ends > 0 and number_found_consecutive_empty_rows < self.number_of_consecutive_empty_rows_to_determine_data_ends))

            row_index += 1

        return worksheet_data

    def get_worksheet_data_as_list_of_lists(self):
        worksheet_data = self.read_rows_until_consecutive_empty_rows()
    
        return worksheet_data

    def get_worksheet_data_as_dict_list(self):
        worksheet_data = self.get_worksheet_data_as_list_of_lists()

        header_names = worksheet_data[0]

        worksheet_dict_list = []

        for i, inner_list in enumerate(worksheet_data):
            if i == 0:
                continue

            row_as_dict = {}
            for j, element in enumerate(inner_list):
                row_as_dict[header_names[j]] = element

            worksheet_dict_list.append(row_as_dict)

        # print(worksheet_dict_list)

        return worksheet_dict_list

    def close_workbook(self):
        self.workbook.close()

    @staticmethod
    def __number_to_excel_column_letter__(number, index_base=1):
        """

        Convert number to its capital ascii character; to be used for Excel row identification.
        1 = A
        2 = B
        etc.
        :param number: integer to be converted to ascii character
        :param index_base: 0 for index starting at 0; 1 for index starting at 1
        :return: single letter (A-Z) or double-letter (ex: AB, DG, etc.)
        :return:
        """
        string = ""

        if index_base < 1:
            number += 1

        while number > 0:
            number, remainder = divmod(number - 1, 26)
            string = chr(65 + remainder) + string
        return string
