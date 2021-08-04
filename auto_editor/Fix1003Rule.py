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
        return project



#----------wenqi without merge in code


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

    # warning handle function name collection
    warning_prefixs_collection = ["CHECK_CUDA((","CUDA_SAFE_CALL((","err = ","CHECK((", "int err ="]

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
                    warning_code = warning_code + now_code
                    warning_code = warning_code.replace("\n", "")

                else:
                    if first_time == False:
                        now_code = all_lines[i].strip()
                    else:
                        now_code = all_lines[i]
                    warning_code = warning_code + now_code+"\n"
                    print("i:",i,",warning_code:",warning_code)
                    new_code = warning_code.split("((")
                    #new_code = warning_code.replace("CHECK_CUDA((", "")
                    new_code = new_code[1].replace(",0));", ";")
                    new_code = new_code.replace(", 0));", ";")
                    new_file.write("#----------------CLA----------\n")
                    new_file.write(new_code)
                    print(new_code)
                    warning_code = ""
                    warning_code_1003 = False
                    first_time = True

                first_time = False
            else:
                new_file.write(all_lines[i])
        else:
            if "*/" in all_lines[i]:
                warning_message_1003 = False
                warning_code_1003 = True

        i += 1

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    old_file_path = "../oneAPI-DirectProgramming-training/ising/dpcpp/main.dp.cpp"
    new_file_path = "../oneAPI-DirectProgramming-training/ising/cla"
    fix_1003(old_file_path,new_file_path)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
