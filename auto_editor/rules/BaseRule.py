from abc import abstractmethod
from typing import List

from enums import CodeChange


class BaseRule:
    def __init__(self):
        self.is_run_complete = False
        self.tracked_changes = []

    def run(self, project_file_paths: List[str]):
        for file_path in project_file_paths:
            self.run_rule(file_path)
        self.is_run_complete = True

    @abstractmethod
    def run_rule(self, file_path: str):
        '''
        contains logic to run the rule on the given file.
        Specifically, loops through each line of the file and checks
        if the rule can be applied related to that line.
        A file can be changed zero, one or multiple times by the rule.

        Where the rule leads to making a comment, use self.insert_comment(...).

        After any change (or comment) was made, use self.track_change(...)
        '''
        pass

    def insert_comment(self, comment_string: str, file_path: str, line_in_file: int):
        # Todo Qichen: add comment insertion logic here
        pass

    def track_change(self):
        '''
        All changes made need to be documented,
        so that this information can be included in the report.
        For this reason, whenever a rule implements a change,
        a new CodeChange item is added to the list.
        '''
        #Todo: implement this. Likely this needs to be implemented individually by each rule.
        pass

    def get_tracked_changes(self) -> List[CodeChange]:
        if not self.is_run_complete:
            raise Exception("Documented change can only be shown after rule was applied!")
        return self.tracked_changes
