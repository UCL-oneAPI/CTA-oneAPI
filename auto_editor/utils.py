from typing import List

from auto_editor.LineItem import LineItem


def get_index_of_line_id(line_id, code_lines: List[LineItem]) -> int:
    for i in range(len(code_lines)):
        if code_lines[i].id == line_id:
            return i
    raise Exception("No line with given ID found.")
