import copy
from abc import abstractmethod
from typing import List
from uuid import uuid4

from auto_editor.LineItem import LineItem
from auto_editor.StructuredProjectSource import StructuredProjectSource
from enums import CodeChange, DiffOperationEnum, ChangeTypeEnum


class BaseRule:
    def __init__(self):
        self.is_run_complete = False
        self.tracked_changes = []

    @property
    @abstractmethod
    def dpct_warning_codes(self) -> List[str]:
        '''
        :return: list of all warning codes on which a rule should be applied, e.g.: ['DPCT1003',]
        '''
        raise Exception("Relevant warning codes not provided for rule.")

    @property
    @abstractmethod
    def change_type(self) -> ChangeTypeEnum:
        raise Exception("This property must be overriden by each rule to state the ChangeTypeEnum.")

    def initiate_run(self, project: StructuredProjectSource):
        current_project_version = project
        for warning_code in self.dpct_warning_codes:
            relevant_warning_locations = current_project_version.dpct_warnings_dict[warning_code] \
                if warning_code in current_project_version.dpct_warnings_dict else []
            for warning in relevant_warning_locations:
                file_path = warning.file_path
                code_lines = current_project_version.paths_to_lines[file_path]

                # index of line id is taken at each iteration,
                # as it may change if the project is modified in preveious iterations
                warning_first_line = self.get_index_of_line_id(warning.first_line_id, code_lines)
                warning_last_line = self.get_index_of_line_id(warning.last_line_id, code_lines)

                # project is updated every time a rule runs, so it always has latest changes.
                # the update for each warning is tracked, so all changes related to that warning can be associated to each other
                old_project_version = copy.deepcopy(current_project_version)
                current_project_version = self.run_rule(current_project_version, warning_first_line, warning_last_line,
                                                        file_path)
                self.track_change(old_project_version, current_project_version)

        self.is_run_complete = True

    @abstractmethod
    def run_rule(self, project: StructuredProjectSource,
                 warning_first_line: int, warning_last_line: int, file_path: str) -> StructuredProjectSource:
        '''
        contains logic to run the rule at the given warning location.
        Changes should be made into project.paths_to_lines

        :return: updated version of project after changes were made
        '''
        pass

    def track_change(self, old_project: StructuredProjectSource, new_project: StructuredProjectSource):
        '''
        All changes made need to be documented,
        so that this information can be included in the report.
        For this reason, whenever a rule implements a change,
        a new CodeChange item is added to the self.tracked_changes list.
        '''
        edit_id = uuid4()
        for path, code_lines in old_project.paths_to_lines.items():
            old_line_ids = set([line.id for line in code_lines])
            new_line_ids = set([line.id for line in new_project.paths_to_lines[path]])
            deleted_line_ids = old_line_ids.difference(new_line_ids)
            added_line_ids = new_line_ids.difference(old_line_ids)

            for line_id in deleted_line_ids:
                change = CodeChange(edit_id=edit_id,
                                    path_to_file=path,
                                    line_id=line_id,
                                    diff_operation=DiffOperationEnum.delete,
                                    rule=self.__class__.__name__,
                                    change_type=self.change_type)
                self.tracked_changes.append(change)

            for line_id in added_line_ids:
                change = CodeChange(edit_id=edit_id,
                                    path_to_file=path,
                                    line_id=line_id,
                                    diff_operation=DiffOperationEnum.add,
                                    rule=self.__class__.__name__,
                                    change_type=self.change_type)
                self.tracked_changes.append(change)

    def get_index_of_line_id(self, id, code_lines: List[LineItem]):
        for i in range(len(code_lines)):
            if code_lines[i].id == id:
                return i
        raise Exception("No line with given ID found.")

    def get_tracked_changes(self) -> List[CodeChange]:
        if not self.is_run_complete:
            raise Exception("Documented change can only be shown after rule was applied!")
        return self.tracked_changes
