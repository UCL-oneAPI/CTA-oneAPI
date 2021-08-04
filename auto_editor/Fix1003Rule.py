from auto_editor.BaseRule import BaseRule
from auto_editor.StructuredProjectSource import StructuredProjectSource
from enums import ChangeTypeEnum


class Fix1003Rule(BaseRule):
    @property
    def dpct_warning_code(self) -> str:
        return "DPCT1003"

    @property
    def change_type(self) -> ChangeTypeEnum:
        return ChangeTypeEnum.fix

    def run_rule(self, project: StructuredProjectSource,
                 warning_first_line: int, warning_last_line: int, file_path: str) -> StructuredProjectSource:
        # Todo: add rule here

        # create a new file for output
        # new_file = open("%s.cla.cpp" % new_file_path, "w")

        remove_function = True

        tmp_dict = project.get_paths_to_lines()

        for file_path in tmp_dict.keys(): # 遍历每个文件
            # all_lines = project.get_paths_to_lines()[file_name]

            all_lines = tmp_dict[file_path]
            code_segment_before_changed = all_lines[warning_last_line + 1]
            for i in range(warning_last_line, len(all_lines)):
                if ";" not in all_lines[i]:
                    if first_time == False:
                        now_code = all_lines[i].strip()
                    else:
                        now_code = all_lines[i]
                        print("prefix code", now_code)
                        prefix = count_prefix(now_code)
                    warning_code = warning_code + now_code
                    warning_code = warning_code.replace("\n", "")
                    first_time = False
                else:
                    if first_time == False:
                        now_code = all_lines[i].strip()
                    else:
                        now_code = all_lines[i]
                        prefix = count_prefix(warning_code)
                    warning_code = warning_code + now_code + "\n"
                    print("i:", i, ",warning_code:", warning_code)

                    if remove_function == True:
                        if "=(" in warning_code:
                            prefix = count_prefix(warning_code)
                            new_code = warning_code.split("=(")
                            merged_warning_code = merge_except_function(new_code)
                            new_code = merged_warning_code.replace(",0);", ";")
                            new_code = new_code.replace(", 0);", ";")
                        elif "= (" in warning_code:
                            prefix = count_prefix(warning_code)
                            new_code = warning_code.split("= (")
                            merged_warning_code = merge_except_function(new_code)
                            new_code = merged_warning_code.replace(",0);", ";")
                            new_code = new_code.replace(", 0);", ";")
                        elif "((" in warning_code:
                            new_code = warning_code.split("((")
                            merged_warning_code = merge_except_function(new_code)
                            new_code = merged_warning_code.replace(",0));", ";")
                            new_code = new_code.replace(", 0));", ";")
                        remove_function == False


                    new_code = prefix + new_code
                    print("prefix", prefix, ".")
                    print(new_code)

                    for j in range(warning_last_line+1,i):
                        all_lines[j] = ""

                    all_lines[warning_last_line+1] = new_code

                    # new_file.write(prefix + "#----------------CLA----------\n")
                    # new_file.write(new_code)
                    warning_code = ""
                    warning_code_1003 = False
                    first_time = True
                tmp_dict[file_path] = all_lines

        project.paths_to_lines = tmp_dict

        return project



#----------wenqi without merge in code


import os

# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import os



def fix_1003(old_file_path,new_file_path):
    lines = open(old_file_path)
    new_file = open("%s.cla.cpp" % new_file_path, "w")

    i = 0
    warning_message_1003 = False # check whether this line is warning message
    warning_code_1003 = False # check whether this line is warning code

    # define the differ_collection
    all_lines = []
    for line in lines:
        line = str(line)
        all_lines.append(line)

    # warning code
    warning_code = ""
    #use to label the origin number of blank before the code
    first_time = True
    remove_function = True


    while i < len(all_lines):
        if warning_message_1003 == False:
            if "/*" in all_lines[i] and "DPCT1003" in all_lines[i+1]:
                warning_message_1003 = True

            elif warning_code_1003 == True:

                if ";" not in all_lines[i]:
                    if first_time == False:
                        now_code = all_lines[i].strip()
                    else:
                        now_code = all_lines[i]
                        print("prefix code",now_code)
                        prefix = count_prefix(now_code)
                    warning_code = warning_code + now_code
                    warning_code = warning_code.replace("\n", "")
                    first_time = False
                else:
                    if first_time == False:
                        now_code = all_lines[i].strip()
                    else:
                        now_code = all_lines[i]
                        prefix = count_prefix(warning_code)
                    warning_code = warning_code + now_code+"\n"
                    print("i:",i,",warning_code:",warning_code)

                    if remove_function == True:
                        if "=(" in warning_code :
                            prefix = count_prefix(warning_code)
                            new_code = warning_code.split("=(")
                            merged_warning_code = merge_except_function(new_code)
                            new_code = merged_warning_code.replace(",0);", ";")
                            new_code = new_code.replace(", 0);", ";")
                        elif "= (" in warning_code :
                            prefix = count_prefix(warning_code)
                            new_code = warning_code.split("= (")
                            merged_warning_code = merge_except_function(new_code)
                            new_code = merged_warning_code.replace(",0);", ";")
                            new_code = new_code.replace(", 0);", ";")
                        elif "((" in warning_code :
                            new_code = warning_code.split("((")
                            merged_warning_code = merge_except_function(new_code)
                            new_code = merged_warning_code.replace(",0));", ";")
                            new_code = new_code.replace(", 0));", ";")
                        remove_function == False

                    new_code = prefix + new_code
                    print("prefix",prefix,".")
                    print(new_code)

                    new_file.write(prefix+"#----------------CLA----------\n")
                    new_file.write(new_code)
                    warning_code = ""
                    warning_code_1003 = False
                    first_time = True


            else:
                new_file.write(all_lines[i])
        else:
            if "*/" in all_lines[i]:
                warning_message_1003 = False
                warning_code_1003 = True

        i += 1

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
        else:
            merged_warning_code = merged_warning_code  + new_code[j]
        j += 1
    print("merged_warning_code:",merged_warning_code)
    return merged_warning_code

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    old_file_path = "../oneAPI-DirectProgramming-training/chi2/dpcpp/chi2.dp.cpp"
    new_file_path = "../oneAPI-DirectProgramming-training/chi2/cla"
    fix_1003(old_file_path,new_file_path)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
