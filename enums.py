from collections import namedtuple

Warning = namedtuple('Warning', 'project_name warning_code file_path message initial_line final_line')

CodeChange = namedtuple('CodeChange', 'change_id edit_id path_to_file line rule change_type')