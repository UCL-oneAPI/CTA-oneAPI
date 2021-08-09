import os
import re
from pathlib import Path
from typing import List, Dict

from auto_editor.LineItem import LineItem
from enums import WarningLocation


class StructuredProjectSource:
    def __init__(self, dpct_root: Path):
        self.dpct_root = dpct_root
        self.paths_to_lines = self.get_paths_to_lines()
        self.dpct_warnings_dict = self.get_dpct_warnings_dict()

    def get_paths_to_lines(self) -> Dict[str, List[LineItem]]:
        '''
        :return: Dict where key = file path, value = list of LineItem instances.
        '''
        file_items = {}
        for file_path in self.get_all_dpct_file_paths():
            line_items = self.get_line_items(file_path)
            file_items[file_path] = line_items
        return file_items

    def get_line_items(self, file_path) -> List[LineItem]:
        line_items = []
        full_file_path = self.dpct_root / file_path
        with open(full_file_path) as f:
            code_lines = f.readlines()
            for i in range(len(code_lines)):
                line_item = LineItem(code=code_lines[i], original_line=i)
                line_items.append(line_item)
        return line_items

    def get_all_dpct_file_paths(self) -> List[str]:
        '''
        Find all (relevant) files in dpct root and its subfolders
        :return: list with paths to all files inside directory at self.dpct_version_root
        '''
        # Todo: use same logic here as in PreAnalyser. Currently nested files aren't discovered.

        paths = []
        test_path = str(self.dpct_root.stem) #'test_project'
        print('path name', test_path)
        num1 = 0
        num2 = 0
        # for file_path in os.listdir(self.dpct_root):
        #     if file_path.endswith(".dp.cpp") or file_path.endswith(".dp.hpp"):
        #         paths.append(file_path)

        for file_dpcpp in self.dpct_root.rglob('*.dp.cpp'):
            temp1 = file_dpcpp.parts
            if test_path in temp1:
                num1 = temp1.index(test_path)
            dpcpp_path = '/'.join(temp1[num1+1:])
            paths.append(dpcpp_path)

        for file_dphpp in self.dpct_root.rglob('*.dp.hpp'):
            temp2 = file_dphpp.parts
            paths.append(str(temp2[-1]))
        for i in paths:
            print(i)

        return paths

    def get_all_file_paths_with_pattern(self, pattern: str):
        pass

    def get_dpct_warnings_dict(self) -> Dict[str, List[WarningLocation]]:
        '''
        :return: Dictionary where keys are strings with dpct warning code.
        Values are lists of WarningLocation instances.
        For the Locations, UIDs instead of lines are used because the lines are changing as warnings are fixed

        E.g.:

        {'DPCT1003': [
            {'first_line_id': uid1, 'last_line_id': uid2, 'file_path': '/main.dp.cpp'},
            {'first_line_id': uid3, 'last_line_id': uid4, 'file_path': '/main.dp.cpp'},
            ]
        'DPCT1065': [
            {'first_line_id': uid5, 'last_line_id': uid6 , 'file_path': '/main.dp.cpp'},
            ]
        }
        '''
        warnings_dict = {}
        for file_path, code_lines in self.paths_to_lines.items():
            for i in range(len(code_lines)):
                line_item = code_lines[i]
                warning_code = line_item.get_dpct_warning_code()
                if warning_code:
                    first_line = self.get_first_warning_line(i, code_lines)
                    last_line = self.get_last_warning_line(i, code_lines)

                    if warning_code not in warnings_dict:
                        warnings_dict[warning_code] = []

                    warnings_dict[warning_code].append(
                        WarningLocation(first_line.id, last_line.id, file_path)
                    )

        return warnings_dict

    def get_first_warning_line(self, any_warning_line: int, code_lines: List[LineItem]) -> LineItem:
        '''
        :param any_warning_line: any line at which there is part of the dpct warning
        :param code_lines: lines for given file
        :return: LineItem of line where warning starts
        '''
        if any_warning_line == 0:
            return code_lines[0]

        start_comment_pattern = "\/\*"

        for i in range(any_warning_line):
            line_index = any_warning_line - i
            code_str = code_lines[line_index].code
            if re.search(start_comment_pattern, code_str):
                return code_lines[line_index]

        raise Exception("Beginning of DPCT warning comment not found!")

    def get_last_warning_line(self, any_warning_line: int, code_lines: List[LineItem]) -> LineItem:
        '''
        :param any_warning_line: any line at which there is part of the dpct warning
        :param code_lines: lines for given file
        :return: LineItem of line where warning ends
        '''
        last_line_in_file = len(code_lines) - 1  # -1 because count starts at zero
        if any_warning_line == last_line_in_file:
            return code_lines[last_line_in_file]

        end_comment_pattern = "\*\/"

        for i in range(any_warning_line + 1, last_line_in_file + 1):
            line_index = i
            code_str = code_lines[line_index].code
            if re.search(end_comment_pattern, code_str):
                return code_lines[line_index]

        raise Exception("End of DPCT warning comment not found!")
