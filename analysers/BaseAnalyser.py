from typing import List


class BaseAnalyser:
    def __init__(self, project_path):
        self.project_path = project_path

    def get_all_warnings(self) -> List[Warning]:
        '''
        :return: list of named tuples with all warnings
        '''
        return []
