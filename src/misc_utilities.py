class MiscUtilities:

    @staticmethod
    def break_list_by_max(self, list_to_break, max_item_count=200):
        start = 0
        end = len(list_to_break)
        result = []
        for x in range(start, end, max_item_count):
            result.append(list_to_break[x:x + max_item_count])
        return result

    @staticmethod
    def break_out_dict_list_by_type_and_max_count(self, dict_list, type_key_name, max_item_count):
        result = []
        column_type_list = sorted(list(set([x.get(type_key_name) for x in dict_list])))
        for column_type in column_type_list:
            typed_list = [x for x in dict_list if column_type == x.get(type_key_name)]
            broken_out_typed_list = MiscUtilities.break_list_by_max(typed_list, max_item_count)
            result.extend(broken_out_typed_list)
