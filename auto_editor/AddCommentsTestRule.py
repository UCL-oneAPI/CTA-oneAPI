from typing import List

from auto_editor.BaseRule import BaseRule
from auto_editor.LineItem import LineItem
from auto_editor.StructuredProjectSource import StructuredProjectSource
from enums import ChangeTypeEnum


class AddCommentsTestRule(BaseRule):
    @property
    def change_type(self) -> ChangeTypeEnum:
        return ChangeTypeEnum.recommendation

    @property
    def dpct_warning_codes(self) -> List[str]:
        return ['DPCT1049']

    def run_rule(self, project: StructuredProjectSource,
                 warning_first_line: int, warning_last_line: int, file_path: str) -> StructuredProjectSource:
        file_lines = project.paths_to_lines[file_path]
        del file_lines[warning_first_line: warning_last_line + 1]
        comment_item = LineItem("This is an insertion in the code! \n")
        file_lines.insert(warning_first_line, comment_item)

        return project
