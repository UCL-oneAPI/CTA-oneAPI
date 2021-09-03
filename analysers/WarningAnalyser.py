from pathlib import Path
from typing import List
from auto_editor.StructuredProjectSource import StructuredProjectSource
from enums import WarningItem


class WarningAnalyser:
    def __init__(self, project_root_path: Path):
        self.project_root_path = project_root_path

    def get_all_warnings(self) -> List[WarningItem]:
        '''
        :return: list of named tuples with all warnings
        '''
        project = StructuredProjectSource(self.project_root_path)
        warnings_dict = project.dpct_warnings_dict
        all_warnings = []
        all_codes = {}
        all_ids = {}

        for name, line_items in project.paths_to_lines.items():
            for i in line_items:
                all_codes.setdefault(name, []).append(i.code)
                all_ids.setdefault(name, []).append(i.id)

        for k, v in warnings_dict.items():
            for info in v:
                first_line_id = info[0]
                last_line_id = info[1]
                file_path = info[2]
                path = '/' + file_path
                if file_path in all_ids.keys():
                    codes = all_codes[file_path]
                    ids = all_ids[file_path]
                    first_line = self.get_first_line_num(first_line_id, codes, ids)
                    message = self.get_warning_message(first_line, last_line_id, codes, ids)
                    warning = WarningItem(project_name=self.project_root_path.stem,
                                          warning_code=k,
                                          file_path=path,
                                          message=message,
                                          line=first_line)
                    all_warnings.append(warning)
        return all_warnings

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
