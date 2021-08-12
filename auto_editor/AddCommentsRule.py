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
        return ['DPCT1049','DPCT1065']

    def run_rule(self, project: StructuredProjectSource,
                 warning_first_line: int, warning_last_line: int, file_path: str) -> StructuredProjectSource:
        # Todo: add rule here
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

                if w_type == "DPCT1049":
                    del all_items[warning_first_line: warning_last_line + 1]
                    comment_item = LineItem("/*This is an insertion in the code!*/\n")
                    all_items.insert(warning_first_line, comment_item)
                    w_type = "DPCT"
                    return project


                if w_type == "DPCT1065":
                    del all_items[warning_first_line: warning_last_line + 1]
                    comment_item = LineItem("/*It works!*/\n")
                    all_items.insert(warning_first_line, comment_item)
                    w_type = "DPCT"
                    return project

        return project
