from typing import List

from auto_editor.BaseRule import BaseRule
from auto_editor.StructuredProjectSource import StructuredProjectSource
from enums import ChangeTypeEnum


class AddCommentsRule(BaseRule):
    @property
    def change_type(self) -> ChangeTypeEnum:
        return ChangeTypeEnum.recommendation

    @property
    def dpct_warning_codes(self) -> List[str]:
        # Todo: add relevant warning codes
        return ['DPCT1111','DPCT1065']

    def run_rule(self, project: StructuredProjectSource,
                 warning_first_line: int, warning_last_line: int, file_path: str) -> StructuredProjectSource:
        # Todo: add rule here
        # print(f'rule runs here. warning first: {warning_first_line}')
        # return project

        state = 0
        w_type = "DPCT"
        new_line_items = list()

        all_line = list()
        for l in project.get_line_items(file_path):
            all_line.append(l.code)

        for i in range(all_line.__len__()):
            line_list = list(all_line[i].split())
            if state == 1:

                # Add if statement for new warning types

                if len(line_list) != 0 and line_list[0].split(':')[0] in self.dpct_warning_codes:
                    w_type = line_list[0].split(':')[0]

            if len(line_list) != 0 and line_list[:1][0] == '/*':
                state = 1
            if state == 1 and len(line_list) != 0 and line_list[-1:][0] == '*/':
                state = 0

                # add if statement for the corresponding warning type, and change the recommendation

                if w_type == "DPCT1111":
                    all_line.insert(int(i) + 1, "/*it is works!*/\n")
                    w_type = "DPCT"

                if w_type == "DPCT1065":
                    all_line.insert(int(i) + 1, "/*it is also works!*/\n")
                    w_type = "DPCT"

        fp_file = open(file_path, 'w+')
        for item in all_line:
            fp_file.write(item)
        fp_file.close()

        project.paths_to_lines = project.get_paths_to_lines()
        project.dpct_warnings_dict = project.get_dpct_warnings_dict()
        return project
