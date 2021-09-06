
from typing import List

from auto_editor.BaseRule import BaseRule
from auto_editor.StructuredProjectSource import StructuredProjectSource
from enums import ChangeTypeEnum
from auto_editor.LineItem import LineItem


class AddCommentsRule(BaseRule):
    @property
    def change_type(self) -> ChangeTypeEnum:
        return ChangeTypeEnum.recommendation

    @property
    def dpct_warning_codes(self) -> List[str]:
        # Add new warning types in this list
        return ['DPCT1065','DPCT1039','DPCT1008','DPCT1000','DPCT1032','DPCT1001','DPCT1009','DPCT1010','DPCT1017']

    def get_indentation_spaces(self,new_code):
        j, prefix = 0, ""
        while j < len(new_code):
            if new_code[j] == " ":
                prefix = prefix + " "
                j += 1
            else:
                break
        return prefix

    def run_rule(self, project: StructuredProjectSource,
                 warning_first_line: int, warning_last_line: int, file_path: str) -> StructuredProjectSource:
        state = False
        w_type = "DPCT"
        count = 0
        all_line = list()
        all_items = project.paths_to_lines[file_path]
        for c in all_items:
            all_line.append(c.code)
        prefix = ''
        for i in range(all_line.__len__())[warning_first_line:]:
            line_list = list(all_line[i].split())
            if state == True:
                if len(line_list) != 0 and line_list[0].split(':')[0] in self.dpct_warning_codes:
                    w_type = line_list[0].split(':')[0]
                    count = line_list[0].split(':')[1]

            if len(line_list) != 0 and line_list[0] == '/*':
                state = True
                prefix = self.get_indentation_spaces(all_line[i])
            if state == True and len(line_list) != 0 and line_list[-1] == '*/':
                state = False

                # add if statement for the corresponding warning type, and change the recommendation
                if w_type == "DPCT1065":
                    del all_items[warning_first_line: warning_last_line + 1]

                    comment_item = LineItem(prefix + "/*\n"
                                                     + prefix + "CTA1065:" + count + ": CTA recommended to ignore this warning. \n"
                                                     + prefix + "but you can also consider replacing 'item_ct1.barrier();' \n"
                                                     + prefix + "with 'item_ct1.barrier(sycl::access::fence_space::local_space);' \n"
                                                     + prefix + "to have have better performance if the kernel function \n"
                                                     + prefix + "has no memory accesses in the global memory.\n"
                                                     + prefix + "*/\n")

                    all_items.insert(warning_first_line, comment_item)
                    w_type = "DPCT"
                    return project

                if w_type == "DPCT1039":
                    del all_items[warning_first_line: warning_last_line + 1]
                    comment_item = LineItem(prefix + "/*\n"
                                                     + prefix + "CTA1039:" + count + ": Based on analysed sample data, strongly recommended to leave the code as it is \n"
                                                     + prefix + "and ignore this warning （27/32 cases）. BUT, if the first parameter of an atomic function points to a local memory address space,\n"
                                                     + prefix + "replace the atomic function name with an atomic function name that includes the template parameters.（5/32 cases）\n"
                                                     + prefix + "*/\n")

                    all_items.insert(warning_first_line, comment_item)
                    w_type = "DPCT"
                    return project


                if w_type == "DPCT1008":
                    del all_items[warning_first_line: warning_last_line + 1]
                    comment_item = LineItem(prefix + "/*\n"
                                                     + prefix + "CTA1008:" + count + ": The clock function is not defined in DPC++, you can leave the code as it is for now. \n"
                                                     + prefix + "And consult with your hardware vendor to find a replacement. 15/15 1008 warnings in CTA analysis data pool choose not to change anything.\n"
                                                     + prefix + "*/\n")

                    all_items.insert(warning_first_line, comment_item)
                    w_type = "DPCT"
                    return project

                if w_type == "DPCT1000":
                    del all_items[warning_first_line: warning_last_line + 1]
                    comment_item = LineItem(prefix + "/*\n"
                                                     + prefix + "CTA1000:" + count + ": Based on analysed sample data, this warning was ignored in 9/9 cases，strongly recommended to ignore this warning.\n"
                                                     + prefix + "*/\n")
                    all_items.insert(warning_first_line, comment_item)
                    w_type = "DPCT"
                    return project

                if w_type == "DPCT1001":
                    del all_items[warning_first_line: warning_last_line + 1]
                    comment_item = LineItem(prefix + "/*\n"
                                                     + prefix + "CTA1001:" + count + ": Based on analysed sample data, this warning was ignored in 9/9 cases，strongly recommended to ignore this warning.\n"
                                                     + prefix + "*/\n")

                    all_items.insert(warning_first_line, comment_item)
                    w_type = "DPCT"
                    return project


                if w_type == "DPCT1032":
                    del all_items[warning_first_line: warning_last_line + 1]
                    comment_item = LineItem(prefix + "/*\n"
                                                     + prefix + "CTA1032:" + count + ": Based on analysed sample data, recommended to ignore this warning（5/8 cases）. If it didn't work, adjust the code.\n"
                                                     + prefix + "*/\n")
                    all_items.insert(warning_first_line, comment_item)
                    w_type = "DPCT"
                    return project

                if w_type == "DPCT1009":
                    del all_items[warning_first_line: warning_last_line + 1]
                    comment_item = LineItem(prefix + "/*\n"
                                                     + prefix + "CTA1009:" + count + ": SYCL uses exceptions to report errors and does not use the error codes. \n"
                                                     + prefix + "The original code was commented out and a warning string was inserted. You need to rewrite this code（1/2 cases）\n"
                                                     + prefix + "*/\n")
                    all_items.insert(warning_first_line, comment_item)
                    w_type = "DPCT"
                    return project

                if w_type == "DPCT1010":
                    del all_items[warning_first_line: warning_last_line + 1]
                    comment_item = LineItem(prefix + "/*\n"
                                                     + prefix + "CTA1010:" + count + ": Based on analysed sample data, in 7/9 cases in the sample data, this warning was ignored, \n"
                                                     + prefix + "so strongly recommended to ignore this warning.\n"
                                                     + prefix + "*/\n")
                    all_items.insert(warning_first_line, comment_item)
                    w_type = "DPCT"
                    return project



                if w_type == "DPCT1017":
                    del all_items[warning_first_line: warning_last_line + 1]
                    comment_item = LineItem(prefix + "/*\n"
                                                     + prefix + "CTA1017:" + count + ": The sycl: sincos call is used instead of the sincosf call. These two calls do not provide exactly the same functionality. \n"
                                                     + prefix + "Check thepotential precision and/or performance issues for the generated code. \n"
                                                     + prefix + "2/2 1017 warnings in CTA analysis data pool choose not to change anything.\n"
                                                     + prefix + "*/\n")

                    all_items.insert(warning_first_line, comment_item)
                    w_type = "DPCT"
                    return project


        return project
