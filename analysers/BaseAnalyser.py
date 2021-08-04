from typing import List

from enums import WarningItem


class BaseAnalyser:
    def __init__(self, project_root_path: str):
        self.project_root_path = project_root_path

    def get_all_warnings(self) -> List[WarningItem]:
        '''
        :return: list of named tuples with all warnings
        '''
        return []
