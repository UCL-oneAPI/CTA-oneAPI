from typing import List

from auto_editor.BaseRule import BaseRule
from auto_editor.StructuredProjectSource import StructuredProjectSource
from enums import ChangeTypeEnum


class Fix1003Rule(BaseRule):
    @property
    def dpct_warning_codes(self) -> List[str]:
        return ["DPCT1003"]

    @property
    def change_type(self) -> ChangeTypeEnum:
        return ChangeTypeEnum.fix

    def run_rule(self, project: StructuredProjectSource,
                 warning_first_line: int, warning_last_line: int, file_path: str) -> StructuredProjectSource:
        # Todo: add rule here
        first_time = True
        warning_code, prefix = "", ""
        tmp_dict = project.paths_to_lines
        all_lines = tmp_dict[file_path]

        for i in range(warning_last_line+1, len(all_lines)):
            print("warning code:",all_lines[i].code)
            if ";" not in all_lines[i].code:
                now_code = self.strip_determin(first_time, all_lines[i])
                warning_code = warning_code + now_code
                warning_code = warning_code.replace("\n", "")
                first_time = False
            else:
                now_code = self.strip_determin( first_time, all_lines[i])
                warning_code = warning_code + now_code + "\n"
                prefix, new_code = self.remove_function_info(warning_code)
                new_code = prefix + new_code
                print("new_code:",new_code)

                self.replace_useless_multiple_line(warning_last_line, i, all_lines)
                all_lines[warning_last_line+1].code = new_code
                self.test_print( all_lines, warning_last_line)
                tmp_dict[file_path] = all_lines
                break

        project.paths_to_lines = tmp_dict
        return project

    def strip_determin(self,first_time,lines):
        if first_time == False:
            now_code = lines.code.strip()
        else:
            now_code = lines.code

        return now_code

    def replace_useless_multiple_line(self,warning_last_line,i,all_lines):
        for j in range(warning_last_line + 1, i + 1):
            temp = all_lines[j]
            temp.code = ""
            all_lines[j] = temp

    def test_print(self,all_lines,warning_last_line):
        print("******Fix1003 Result****")
        print("all_lines[",warning_last_line,"]:", all_lines[warning_last_line ].code)
        print("all_lines[",warning_last_line+1,"]:", all_lines[warning_last_line + 1].code)
        print("all_lines[",warning_last_line+2,"]:", all_lines[warning_last_line + 2].code)
        print("all_lines[",warning_last_line+3,"]:", all_lines[warning_last_line + 3].code)

    def remove_function_info(self, warning_code):
        prefix = count_prefix(warning_code)
        new_code = warning_code
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
            merged_warning_code = merge_except_function(new_code)
            new_code = merged_warning_code.replace(",0));", ";")
            new_code = new_code.replace(", 0));", ";")
        else:
            merged_warning_code = merge_except_function(new_code)
            new_code = merged_warning_code.replace(",0);", ";")
            new_code = new_code.replace(", 0);", ";")

        return new_code


def count_prefix(new_code):
    j, prefix = 0, ""
    while j < len(new_code):
        if new_code[j] == " ":
            prefix = prefix + " "
            j += 1
        else:
            break

    return prefix

def merge_except_function(new_code):
    j, merged_warning_code = 1, ""
    while j < len(new_code):
        if j >1:
            merged_warning_code = merged_warning_code + "=(" +new_code[j]
        else:
            merged_warning_code = merged_warning_code + new_code[j]
        j += 1
    #print("merged_warning_code:", merged_warning_code)
    return merged_warning_code




