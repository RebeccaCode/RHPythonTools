class AwsAthenaUtilities:

    @staticmethod
    def build_pivot_query(broken_out_typed_list, database_dot_table_name, key_column_name, value_column_name):
        group_subquery_dict = AwsAthenaUtilities.__build_pivot_query_group_subquery_string_dict__(
            broken_out_typed_list=broken_out_typed_list,
            key_column_name=key_column_name,
            column_name_to_be_counted=value_column_name,
            database__dot_table_name=database_dot_table_name)
        
        all_subquery_strings = '\n, '.join(list(group_subquery_dict.values()))
        
        union_subquery_template = \
"""
select column_name, try_cast(column_value as varchar) as column_value, column_value_count from group{group_number}
"""     
        union_subquery_list = []
        for group_number in group_subquery_dict.keys():
            union_subquery = union_subquery_template.format(group_number=group_number)
            union_subquery_list.append(union_subquery)
        union_strings = '\nunion all\n'.join(union_subquery_list)
        main_query_template = \
f"""
with 
{all_subquery_strings}
{union_strings}
"""
        
        result = main_query_template.format(all_subquery_strings=all_subquery_strings,
                                            union_strings=union_strings)
        
        return result
        

    @staticmethod
    def __build_pivot_query_group_subquery_string_dict__(broken_out_typed_list, key_column_name,
                                                         column_name_to_be_counted, database__dot_table_name):
        query_substring_template = \
            f"""
group{group_number} (data_source_column_nam, column_value, column_value_count) as (
  select t.column_name,
         coalesce(try_cast(t.column_value as varchar), '') as column_value,
         count(distinct(tbl.{column_to_be_counted})) as column_value_count
    from {database__dot_table_name} tbl
    cross join unnest (
      array[{single_quoted_column_list_string}],
      array[{double_quoted_column_list_string}]
      ) t(column_name, column_value)
  group by t.column_name,
           t.column_value
) 
"""
        result = {}
        for i, broken_out_list in enumerate(broken_out_typed_list):
            column_name_list = [x.get(key_column_name) for x in broken_out_list]
            single_quoted_column_list_string = ','.join([f'\'{x}\'' for x in column_name_list])
            double_quoted_column_list_string = ','.join([f'"{x}"' for x in column_name_list])

            group_subquery = query_substring_template.format(group_number=i,
                                                             column_name_to_be_counted=column_name_to_be_counted,
                                                             database__dot_table_name=database__dot_table_name,
                                                             single_quoted_column_list_string=single_quoted_column_list_string,
                                                             double_quoted_column_list_string=double_quoted_column_list_string)

            result[i] = group_subquery

        return result
