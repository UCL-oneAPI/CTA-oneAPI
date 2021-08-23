# from typing import List
#
# from auto_editor.BaseRule import BaseRule
# from auto_editor.StructuredProjectSource import StructuredProjectSource
# from enums import ChangeTypeEnum
# from auto_editor.LineItem import LineItem
#
#
# class AddCommentsRule(BaseRule):
#     @property
#     def change_type(self) -> ChangeTypeEnum:
#         return ChangeTypeEnum.recommendation
#
#     @property
#     def dpct_warning_codes(self) -> List[str]:
#         # Todo: add relevant warning codes
#         # Add new warning types in this list
#         return ['DPCT1049','DPCT1065']
#
#     def run_rule(self, project: StructuredProjectSource,
#                  warning_first_line: int, warning_last_line: int, file_path: str) -> StructuredProjectSource:
#         # Todo Qichen: fix rule
#         state = False
#         w_type = "DPCT"
#         all_line = list()
#         all_items = project.paths_to_lines[file_path]
#         for c in all_items:
#             all_line.append(c.code)
#
#         for i in range(all_line.__len__()):
#             line_list = list(all_line[i].split())
#             if state == True:
#                 if len(line_list) != 0 and line_list[0].split(':')[0] in self.dpct_warning_codes:
#                     w_type = line_list[0].split(':')[0]
#
#             if len(line_list) != 0 and line_list[0] == '/*':
#                 state = True
#             if state == True and len(line_list) != 0 and line_list[-1] == '*/':
#                 state = False
#
#                 # add if statement for the corresponding warning type, and change the recommendation
#
#                 if w_type == "DPCT1049":
#                     del all_items[warning_first_line: warning_last_line + 1]
#                     comment_item = LineItem("/*This is an insertion in the code!*/\n")
#                     all_items.insert(warning_first_line, comment_item)
#                     w_type = "DPCT"
#                     return project
#
#
#                 if w_type == "DPCT1065":
#                     del all_items[warning_first_line: warning_last_line + 1]
#                     comment_item = LineItem("/*It works!*/\n")
#                     all_items.insert(warning_first_line, comment_item)
#                     w_type = "DPCT"
#                     return project
#
#
#         return project
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
        # Todo: add relevant warning codes
        # Add new warning types in this list
        return ['DPCT1065','DPCT1039','DPCT1008','DPCT1000','DPCT1032','DPCT1001']

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
        # Todo Qichen: fix rule
        state = False
        w_type = "DPCT"
        count = 0
        all_line = list()
        all_items = project.paths_to_lines[file_path]
        for c in all_items:
            all_line.append(c.code)
        prefix = ''
        for i in range(all_line.__len__()):
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
                                                     + prefix + "CTA1039:" + count + ": Base on the experience, strongly recommended to leave the code as it is \n"
                                                     + prefix + "and ignore this warning. BUT, if the first parameter of an atomic function points to a local memory address space,\n"
                                                     + prefix + "replace the atomic function name with an atomic function name that includes the template parameters.\n"
                                                     + prefix + "*/\n")

                    all_items.insert(warning_first_line, comment_item)
                    w_type = "DPCT"
                    return project


                if w_type == "DPCT1008":
                    del all_items[warning_first_line: warning_last_line + 1]
                    comment_item = LineItem(prefix + "/*\n"
                                                     + prefix + "CTA1008:" + count + ": The clock function is not defined in DPC++, you can leave the code as it is for now. \n"
                                                     + prefix + "And consult with your hardware vendor to find a replacement.\n"
                                                     + prefix + "*/\n")

                    all_items.insert(warning_first_line, comment_item)
                    w_type = "DPCT"
                    return project

                if w_type == "DPCT1000":
                    del all_items[warning_first_line: warning_last_line + 1]
                    comment_item = LineItem(prefix + "/*\n"
                                                     + prefix + "CTA1000:" + count + ": Base on the experience, strongly recommended to ignore this warning.\n"
                                                     + prefix + "*/\n")
                    all_items.insert(warning_first_line, comment_item)
                    w_type = "DPCT"
                    return project

                if w_type == "DPCT1001":
                    del all_items[warning_first_line: warning_last_line + 1]
                    comment_item = LineItem(prefix + "/*\n"
                                                     + prefix + "CTA1001:" + count + ": Base on the experience, strongly recommended to ignore this warning.\n"
                                                     + prefix + "*/\n")

                    all_items.insert(warning_first_line, comment_item)
                    w_type = "DPCT"
                    return project


                if w_type == "DPCT1032":
                    del all_items[warning_first_line: warning_last_line + 1]
                    comment_item = LineItem(prefix + "/*\n"
                                                     + prefix + "CTA1032:" + count + ": Base on the experience, recommended to ignore this warning. If it didn't work, adjust the code.\n"
                                                     + prefix + "*/\n")

                    all_items.insert(warning_first_line, comment_item)
                    w_type = "DPCT"
                    return project


        return project
