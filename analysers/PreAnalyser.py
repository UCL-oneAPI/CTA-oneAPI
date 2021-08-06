from typing import List

from analysers.BaseAnalyser import BaseAnalyser
from auto_editor.StructuredProjectSource import StructuredProjectSource
from enums import WarningItem


class PreAnalyser(BaseAnalyser):
    def get_all_warnings(self) -> List[WarningItem]:
        '''
        This creates the data for the report of dpct warnings.
        It analyses the project in self.project_root_path.
        :return: list of named tuples WarningItem, one WarningItem for each warning in the project
        '''

        project = StructuredProjectSource(self.project_root_path)
        warnings_dict = project.dpct_warnings_dict

        # TODO Yifei: transform warnings_dict to all_warnings below

        warning = WarningItem(project_name="test_project",
                              warning_code="DPCT1111",
                              file_path='/kernel_wrapper2.dp.cpp',
                              message="DPCT1111:3: The workgroup size passed to the SYCL kernel may exceed the limit.\n"
                                      "To get the device limit, query info::device::max_work_group_size. Adjust the\n"
                                      "workgroup size if needed.",
                              line=127)
        all_warnings = [warning]

        return all_warnings
