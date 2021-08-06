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
        return ['DPCT1065', 'DPCT1010']

    def run_rule(self, project: StructuredProjectSource,
                 warning_first_line: int, warning_last_line: int, file_path: str) -> StructuredProjectSource:
        # Todo: add rule here
        return project
