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
        # Todo: add rule here
        print('-----------------------------------------------------------------------------------------------')
        first_time = True
        warning_code, prefix = "", ""
        self.all_lines = project.paths_to_lines[file_path]
        warning_begin_id = self.all_lines[warning_first_line].id
        warning_end_id = self.all_lines[warning_last_line].id
        print('warning_first_line: ',warning_first_line,' ; warning_last_line: ',warning_last_line)
        one_line_warning_code = True

        for i in range(warning_last_line + 1, len(self.all_lines)):
            print("warning code:",self.all_lines[i].code)
            if ";" not in self.all_lines[i].code:
                now_code = self.strip_determin(first_time, self.all_lines[i])
                warning_code = warning_code + now_code
                warning_code = warning_code.replace("\n", "")
                first_time = False
                one_line_warning_code = False
            else:
                now_code = self.strip_determin( first_time, self.all_lines[i])
                if one_line_warning_code == False:
                    warning_code = warning_code + now_code + "\n"
                else:
                    warning_code = now_code
                prefix, new_code = self.remove_function_info(warning_code)
                new_code = prefix + new_code
                print("new_code:",new_code)

                warning_begin_index = self.delete_dpct_warning(warning_begin_id, warning_end_id)
                print('warning_begin_index',warning_begin_index)
                new_lineItem = LineItem(new_code)
                #self.all_lines.insert(i_position,new_lineItem)
                self.all_lines[warning_begin_index] = new_lineItem

                break

        project.paths_to_lines[file_path] = self.all_lines
        print('length: ',len(project.paths_to_lines[file_path]))
        return project

    def find_true_originline_number(self,all_lines,warning_last_line):
        for i in range( len(all_lines)):
            if all_lines[i].original_line == warning_last_line:
                 return i
        return 0

    def strip_determin(self,first_time,lines):
        if first_time == False:
            now_code = lines.code.strip()
        else:
            now_code = lines.code

        return now_code

    def replace_useless_multiple_line(self,k,i,all_lines):
        del all_lines[k+1:i+1]
        return k+1

    def remove_code(self, first_line: int, last_line: int = None):
        remaining_line = last_line + 1 if last_line else first_line + 1
        del self.all_lines[first_line: remaining_line]

    def delete_dpct_warning(self, warning_begin_id, warning_end_id):
        warning_begin_i = get_index_of_line_id(warning_begin_id, self.all_lines)
        warning_end_i = get_index_of_line_id(warning_end_id, self.all_lines)
        self.remove_code(warning_begin_i, warning_end_i)
        return warning_begin_i

    # def get_index_of_line_id(line_id, code_lines: List[LineItem]) -> int:
    #     for i in range(len(code_lines)):
    #         if code_lines[i].id == line_id:
    #             return i
    #     raise Exception("No line with given ID found.")
    #
    # def remove_code(self, first_line: int, last_line: int = None):
    #     remaining_line = last_line + 1 if last_line else first_line + 1
    #     print("remove", self.file_lines[first_line: remaining_line])
    #     del self.file_lines[first_line: remaining_line]
    #
    # def delete_dpct_warning(self, warning_begin_id, warning_end_id):
    #     warning_begin_i = self.get_index_of_line_id(warning_begin_id, self.file_lines)
    #     warning_end_i = self.get_index_of_line_id(warning_end_id, self.file_lines)
    #     self.remove_code(warning_begin_i, warning_end_i)




    def remove_function_info(self, warning_code):
        new_code = warning_code
        prefix = self.get_indentation_spaces(new_code)
        if "=(" in warning_code:
            new_code = self.replace_condition("=(", warning_code)
        elif "= (" in warning_code:
            new_code = self.replace_condition("= (", warning_code)
        elif "((" in warning_code:
            new_code = self.replace_condition("((", warning_code)

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


    def get_indentation_spaces(self,new_code):
        j, prefix = 0, ""
        while j < len(new_code):
            if new_code[j] == " ":
                prefix = prefix + " "
                j += 1
            else:
                break
        return prefix

    def merge_except_function(self,new_code):
        j, merged_warning_code = 1, ""
        while j < len(new_code):
            if j >1:
                merged_warning_code = merged_warning_code + "=(" +new_code[j]
            else:
                merged_warning_code = merged_warning_code + new_code[j]
            j += 1
        #print("merged_warning_code:", merged_warning_code)
        return merged_warning_code




