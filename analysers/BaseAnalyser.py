from pathlib import Path
from typing import List

from enums import WarningItem


class BaseAnalyser:
    def __init__(self, project_root_path: Path):
        self.project_root_path = project_root_path

    def get_all_warnings(self) -> List[WarningItem]:
        '''
        :return: list of named tuples with all warnings
        '''
        return []

    def get_first_line_num(self, first_id, codes, ids):
        first = 0
        if first_id in ids:
            first = ids.index(first_id) + 2
        return first

    def get_warning_message(self, first, last_info, codes, ids):
        message = ""
        last = 0
        if last_info in ids:
            last = ids.index(last_info)
        for i in range(first-1, last-1):
            message += codes[i].strip() + '\n'
        message += codes[last - 1].strip()
        return message
