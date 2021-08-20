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

    def run_rule(self, project: StructuredProjectSource,
                 warning_first_line: int, warning_last_line: int, file_path: str) -> StructuredProjectSource:
        # Todo Qichen: fix rule
        state = False
        w_type = "DPCT"
        all_line = list()
        all_items = project.paths_to_lines[file_path]
        for c in all_items:
            all_line.append(c.code)

        for i in range(all_line.__len__()):
            line_list = list(all_line[i].split())
            if state == True:
                if len(line_list) != 0 and line_list[0].split(':')[0] in self.dpct_warning_codes:
                    w_type = line_list[0].split(':')[0]

            if len(line_list) != 0 and line_list[0] == '/*':
                state = True
            if state == True and len(line_list) != 0 and line_list[-1] == '*/':
                state = False

                # add if statement for the corresponding warning type, and change the recommendation
                if w_type == "DPCT1065":
                    del all_items[warning_first_line - 1: warning_last_line]
                    comment_item = LineItem("/*CTA1065:count number: recommended to ignore this warning. but you can also consider replacing 'item_ct1.barrier();' with 'item_ct1.barrier(sycl::access::fence_space::local_space);'*/\n")
                    all_items.insert(warning_first_line - 1, comment_item)
                    w_type = "DPCT"
                    return project

                if w_type == "DPCT1039":
                    del all_items[warning_first_line - 1: warning_last_line]
                    comment_item = LineItem("/*CTA1039:count number: Base on the experience, strongly recommended to leave the code as it is and ignore this warning. BUT, if '&xxx' points to local memory, please accept the DPCT proposal.*/\n")
                    all_items.insert(warning_first_line - 1, comment_item)
                    w_type = "DPCT"
                    return project

                if w_type == "DPCT1008":
                    del all_items[warning_first_line - 1: warning_last_line]
                    comment_item = LineItem("/*CTA1008:count number:Please accept the DPCT proposal.  You can leave the code as it is for now.*/\n")
                    all_items.insert(warning_first_line - 1, comment_item)
                    w_type = "DPCT"
                    return project

                if w_type == "DPCT1000":
                    del all_items[warning_first_line - 1: warning_last_line]
                    comment_item = LineItem("/*CTA1000:count number: Base on the experience, strongly recommended to ignore this warning.*/\n")
                    all_items.insert(warning_first_line - 1, comment_item)
                    w_type = "DPCT"
                    return project

                if w_type == "DPCT1001":
                    del all_items[warning_first_line - 1: warning_last_line]
                    comment_item = LineItem("/*CTA1001:count number: Base on the experience, strongly recommended to ignore this warning.*/\n")
                    all_items.insert(warning_first_line - 1, comment_item)
                    w_type = "DPCT"
                    return project

                if w_type == "DPCT1032":
                    del all_items[warning_first_line - 1: warning_last_line]
                    comment_item = LineItem("/*CTA1032:count number: Base on the experience, recommended to ignore this warning. If it didn't work, adjust the code.*/\n")
                    all_items.insert(warning_first_line - 1, comment_item)
                    w_type = "DPCT"
                    return project


        return project
