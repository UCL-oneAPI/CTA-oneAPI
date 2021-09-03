from typing import List

from auto_editor.BaseRule import BaseRule
from auto_editor.LineItem import LineItem
from auto_editor.StructuredProjectSource import StructuredProjectSource
from enums import ChangeTypeEnum
from auto_editor.utils import get_index_of_line_id


class Fix1003Rule(BaseRule):
    def __init__(self):
        super().__init__()
        self.all_lines = []

    @property
    def dpct_warning_codes(self) -> List[str]:
        return ["DPCT1003"]

    @property
    def change_type(self) -> ChangeTypeEnum:
        return ChangeTypeEnum.fix

    def run_rule(self, project: StructuredProjectSource,
                 warning_first_line: int, warning_last_line: int, file_path: str) -> StructuredProjectSource:
        print('-----------------------------------------------------------------------------------------------')
        first_time = True
        warning_code, prefix = "", ""
        tmp_dict = project.paths_to_lines
        self.all_lines = tmp_dict[file_path]
        other_warnings = self.get_other_warnings(warning_first_line, project)
        one_line_warning_code = True

        for i in range(warning_last_line + 1, len(self.all_lines)):
            if ";" not in self.all_lines[i].code:
                now_code = self.strip_determin(first_time, self.all_lines[i])
                warning_code = warning_code + now_code
                warning_code = warning_code.replace("\n", "")
                first_time = False
                one_line_warning_code = False
            else:
                now_code = self.strip_determin(first_time, self.all_lines[i])
                if one_line_warning_code == False:
                    warning_code = warning_code + now_code + "\n"
                else:
                    warning_code = now_code
                prefix, new_code = self.remove_function_info(warning_code)
                new_code = prefix + new_code

                # remove old statement
                self.remove_obsolete_code(i, warning_last_line, self.all_lines, other_warnings)

                # remove old warning message
                self.remove_code(self.all_lines, warning_first_line, warning_last_line)

                new_lineItem = LineItem(new_code)
                self.all_lines.insert(warning_first_line, new_lineItem)
                tmp_dict[file_path] = self.all_lines
                break

        project.paths_to_lines[file_path] = tmp_dict[file_path]
        return project

    def get_other_warnings(self, warning_first_line, project):
        other_warnings = []
        current_warning_line_id = self.all_lines[warning_first_line].id
        for warning_code, warning_list in project.dpct_warnings_dict.items():
            for warning in warning_list:
                if not warning.first_line_id == current_warning_line_id:
                    other_warnings.append(warning)
        return other_warnings

    def find_true_originline_number(self, all_lines, warning_last_line):
        for i in range(len(all_lines)):
            if all_lines[i].original_line == warning_last_line:
                return i
        return 0

    def strip_determin(self, first_time, lines):
        if first_time == False:
            now_code = lines.code.strip()
        else:
            now_code = lines.code

        return now_code

    def remove_obsolete_code(self, old_statement_end, warning_last_line, all_lines, other_warnings):
        first_deletable_line = warning_last_line + 1
        for line_i in range(first_deletable_line, old_statement_end + 1):
            # in rare edge cases, multiple warnings exist one after another,
            # referring to the same subsequent line of code (e.g. vmc sample project).
            # If that happens, this method must not delete the subsequent warning, but only the statement below,
            # as that statement will be replaced later on.
            for warning in other_warnings:
                if warning.first_line_id == all_lines[line_i].id:
                    last_warning_line = get_index_of_line_id(warning.last_line_id, all_lines)
                    first_deletable_line = last_warning_line + 1
                    break

        del all_lines[first_deletable_line:old_statement_end + 1]

    def remove_function_info(self, warning_code):
        new_code = warning_code
        prefix = self.get_indentation_spaces(new_code)

        if "((" in warning_code:
            new_code = self.replace_condition("((", warning_code)
        elif "( (" in warning_code:
            new_code = self.replace_condition("((", warning_code)
        elif "=(" in warning_code:
            new_code = self.replace_condition("=(", warning_code)
        elif "= (" in warning_code:
            new_code = self.replace_condition("= (", warning_code)

        return prefix, new_code

    def replace_condition(self, type, warning_code):
        new_code = warning_code.split(type)
        if type == "((":
            merged_warning_code = self.merge_except_function(new_code)
            new_code = merged_warning_code.replace(",0));", ";")
            new_code = new_code.replace(", 0));", ";")
        else:
            merged_warning_code = self.merge_except_function(new_code)
            new_code = merged_warning_code.replace(",0);", ";")
            new_code = new_code.replace(", 0);", ";")

        return new_code

    def get_indentation_spaces(self, new_code):
        j, prefix = 0, ""
        while j < len(new_code):
            if new_code[j] == " ":
                prefix = prefix + " "
                j += 1
            else:
                break
        return prefix

    def merge_except_function(self, new_code):
        j, merged_warning_code = 1, ""
        while j < len(new_code):
            if j > 1:
                merged_warning_code = merged_warning_code + "=(" + new_code[j]
            else:
                merged_warning_code = merged_warning_code + new_code[j]
            j += 1
        return merged_warning_code
