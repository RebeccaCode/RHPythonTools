import csv
import json

class CsvUtilities:

    @staticmethod
    def write_csv_from_dict(the_dict, file_path, delimiter='|'):
        if not the_dict or len(the_dict) < 1:
            return
        the_path = file_path if file_path.endswith('.csv') else f'{file_path}.csv'
        header = list(the_dict[0].keys())
        with open(the_path, 'w', encoding='utf8', newline='') as f:
            csv_writer = csv.DictWriter(f, fieldnames=header, delimiter=delimiter)
            csv_writer.writeheader()
            csv_writer.writerows(the_dict)

    @staticmethod
    def write_json_from_dict_list_each_element_single_line(the_dict, file_path):
        if not the_dict or len(the_dict) < 1:
            return
        the_path = file_path if file_path.endswith('.json') else f'{file_path}.json'
        with open(the_path, 'w', encoding='utf8') as f:
            f.write(
                '[' +
                ',\n'.join(json.dumps(i) for i in the_dict) +
                ']')

    @staticmethod
    def write_json_from_dict_multiple_lines(the_dict, file_path):
        if not the_dict or len(the_dict) < 1:
            return
        the_path = file_path if file_path.endswith('.json') else f'{file_path}.json'
        with open(the_path, 'w', encoding='utf8') as f:
            f.write(json.dumps(the_dict, default=lambda o: o.__dict__, indent=4))

    @staticmethod
    def write_csv_json_from_dict(the_dict, file_path, delimiter='|'):
        write_csv_from_dict(the_dict, file_path, delimiter)
        write_json_from_dict(the_dict, file_path)

    @staticmethod
    def read_csv_to_list_of_dict(csv_file_path, delimiter='|'):
        with open(csv_file_path) as f:
            dict_reader = csv.DictReader(f, delimiter=delimiter)
        return list(dict_reader)

    @staticmethod
    def break_list_by_max(list_to_break, max_attribute_count=200):
        start = 0
        end = len(list_to_break)
        result = []
        for i in range(start, end, max_attribute_count):
            x = i
            result.append(list_to_break[x:x + max_attribute_count])
        return result
