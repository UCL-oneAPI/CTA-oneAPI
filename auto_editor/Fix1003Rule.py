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

        remove_function = True
        first_time = True
        warning_code, prefix = "", ""
        tmp_dict = project.paths_to_lines
        all_lines = tmp_dict[file_path]
        #code_segment_before_changed = all_lines[warning_last_line + 1]

        for i in range(warning_last_line+1, len(all_lines)):
            print("warning code:",all_lines[i].code)
            if ";" not in all_lines[i].code:
                if first_time == False:
                    now_code = all_lines[i].code.strip()
                else:
                    now_code = all_lines[i].code
                    print("prefix code", now_code)
                    prefix = count_prefix(now_code)
                warning_code = warning_code + now_code
                warning_code = warning_code.replace("\n", "")
                first_time = False
            else:
                if first_time == False:
                    now_code = all_lines[i].code.strip()
                else:
                    now_code = all_lines[i].code
                    prefix = count_prefix(warning_code)

                warning_code = warning_code + now_code + "\n"

                if remove_function == True:
                    prefix, new_code = self.remove_function_info(warning_code)
                    remove_function = False

                new_code = prefix + new_code
                print("new_code:",new_code)

                for j in range(warning_last_line+1,i):
                    print("j:",j)
                    temp = all_lines[j]
                    temp.code = ""
                    all_lines[j] = temp

                print("warning_last_line+1",warning_last_line+1)
                all_lines[warning_last_line+1].code = new_code
                print("all_lines[warning_last_line+1]:",all_lines[warning_last_line+1].code)

                warning_code = ""
                warning_code_1003 = False
                first_time = True

                tmp_dict[file_path] = all_lines

                break

        project.paths_to_lines = tmp_dict
        return project

    def remove_function_info(self, warning_code):
        prefix = ""
        new_code = warning_code
        if "=(" in warning_code:
            prefix = count_prefix(warning_code)
            new_code = self.replace_condition("=(", warning_code)
        elif "= (" in warning_code:
            prefix = count_prefix(warning_code)
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
        #print("j is :",new_code[j])
        if new_code[j] == " ":
            prefix = prefix + " "
            j += 1
            #print("1")
        else:
            break

    return prefix

def merge_except_function(new_code):
    j, merged_warning_code = 1, ""
    while j < len(new_code):
        #print("j is :",new_code[j])
        if j >1:
            merged_warning_code = merged_warning_code + "=(" +new_code[j]
            #print("1---",merged_warning_code)
        else:
            #print("2.1---", merged_warning_code,", new_code[j]:--",new_code[j])
            merged_warning_code = merged_warning_code + new_code[j]
            #print("2.2---", merged_warning_code)
        j += 1
    print("merged_warning_code:", merged_warning_code)
    return merged_warning_code

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    old_file_path = "../oneAPI-DirectProgramming-training/chi2/dpcpp/chi2.dp.cpp"
    new_file_path = "../oneAPI-DirectProgramming-training/chi2/cla"
    fix_1003(old_file_path,new_file_path)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
