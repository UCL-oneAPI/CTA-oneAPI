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
        return ['DPCT1065', 'DPCT1010']

    def run_rule(self, project: StructuredProjectSource,
                 warning_first_line: int, warning_last_line: int, file_path: str) -> StructuredProjectSource:
        # Todo: add rule here
        file_path = ".\kernel_wrapper2.dp.cpp"
        state = 0
        w_type = "DPCT"
        new_line_items = list()
        print(project.paths_to_lines[file_path][0].code)
        print(project.get_line_items(file_path)[0].code)
        print("1")
        for i in range(project.get_line_items(file_path).__len__()):
            line_list = list(project.get_line_items(file_path)[i].code.split())
            if state == 1:

                # Add if statement for new warning types

                if len(line_list) != 0 and line_list[0].split(':')[0] in self.dpct_warning_codes:
                    w_type = line_list[0].split(':')[0]

            if len(line_list) != 0 and line_list[:1][0] == '/*':
                state = 1
            if state == 1 and len(line_list) != 0 and line_list[-1:][0] == '*/':
                state = 0

                # add if statement for the corresponding warning type, and change the recommendation

                if w_type == "DPCT1065":
                    new_line_items = project.get_line_items(file_path).insert(int(i) + 1, "/*it is works!*/\n")
                    w_type = "DPCT"

        fp_file = open(file_path, 'w+')
        for item in new_line_items:
            fp_file.write(item)
        fp_file.close()
        return project

if __name__ == '__main__':
    line_items = []
    full_file_path = ".\kernel_wrapper2.dp.cpp"
    with open(full_file_path) as f:
        code_lines = f.readlines()
        for i in range(len(code_lines)):
            line_item = LineItem(code=code_lines[i], original_line=i)
            line_items.append(line_item)
    addComment = AddCommentsRule()
    print(addComment.run_rule(line_item,0,0,full_file_path))
