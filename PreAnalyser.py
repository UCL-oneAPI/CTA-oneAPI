from typing import List

from analysers.BaseAnalyser import BaseAnalyser
from auto_editor.StructuredProjectSource import StructuredProjectSource
from enums import WarningItem

import re


class PreAnalyser(BaseAnalyser):
    def get_all_warnings(self) -> List[WarningItem]:
        '''
        This creates the data for the report of dpct warnings.
        It analyses the project in self.project_root_path.
        :return: list of named tuples WarningItem, one WarningItem for each warning in the project
        '''

        project = StructuredProjectSource(self.project_root_path)
        warnings_dict = project.dpct_warnings_dict
        codes = []
        ids = []
        for i in project.paths_to_lines.values():
            for j in i:
                codes.append(j.code)
                ids.append(j.id)
        # TODO Yifei: transform warnings_dict to all_warnings below
        all_warnings = []

        for k, v in warnings_dict.items():
            for info in v:
                path = '/'+info[2]
                first_line = self.get_first_line_num(info[0], codes, ids)
                message = self.get_warning_message(first_line, info[1], codes, ids)
                warning = WarningItem(project_name=self.project_root_path.stem,
                                      warning_code=k,
                                      file_path=path,
                                      message=message,
                                      # "DPCT1111:3: The workgroup size passed to the SYCL kernel may exceed the limit.\n"
                                      #         "To get the device limit, query info::device::max_work_group_size. Adjust the\n"
                                      #         "workgroup size if needed.",
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
