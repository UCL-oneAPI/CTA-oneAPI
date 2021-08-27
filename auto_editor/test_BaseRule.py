import copy
import unittest

from auto_editor.Fix1049Rule import Fix1049Rule
from auto_editor.LineItem import LineItem
from auto_editor.StructuredProjectSource import StructuredProjectSource
from enums import DiffOperationEnum, ChangeTypeEnum
from testing_support.BaseTest import BaseTest


class TestBaseRule(BaseTest):
    def get_project_by_path(self, p):
        path = self.get_full_test_path(p)
        return StructuredProjectSource(path)

    def test_trackChange_lineAdded_changeTracked(self):
        old_version = self.get_project_by_path("unit_testing_data/base_rule_testing/simple_project")
        new_version = copy.deepcopy(old_version)
        new_line = LineItem(code="some changed code line")
        new_version.paths_to_lines['some_file.dp.cpp'].append(new_line)
        base_rule = Fix1049Rule()

        self.assertEqual([], base_rule.tracked_changes)
        base_rule.track_change(old_version, new_version)
        self.assertEqual(1, len(base_rule.tracked_changes))
        self.assertEqual(DiffOperationEnum.add, base_rule.tracked_changes[0].diff_operation)
        self.assertEqual(ChangeTypeEnum.fix, base_rule.tracked_changes[0].change_type)

    def test_trackChange_lineDeleted_changeTracked(self):
        old_version = self.get_project_by_path("unit_testing_data/base_rule_testing/simple_project")
        new_version = copy.deepcopy(old_version)
        new_version.paths_to_lines['some_file.dp.cpp'].pop()  # delete last line
        base_rule = Fix1049Rule()

        self.assertEqual([], base_rule.tracked_changes)
        base_rule.track_change(old_version, new_version)
        self.assertEqual(1, len(base_rule.tracked_changes))

    def test_trackChange_multipleChanges_changesTracked(self):
        old_version = self.get_project_by_path("unit_testing_data/base_rule_testing/simple_project")
        new_version = copy.deepcopy(old_version)
        new_version.paths_to_lines['some_file.dp.cpp'].pop()  # delete last line
        new_line = LineItem(code="some changed code line")
        new_version.paths_to_lines['some_file.dp.cpp'].append(new_line)
        base_rule = Fix1049Rule()

        self.assertEqual([], base_rule.tracked_changes)
        base_rule.track_change(old_version, new_version)
        self.assertEqual(2, len(base_rule.tracked_changes))

    def test_trackChange_noChangesExist_noChangesTracked(self):
        old_version = self.get_project_by_path("unit_testing_data/base_rule_testing/simple_project")
        new_version = copy.deepcopy(old_version)
        base_rule = Fix1049Rule()

        self.assertEqual([], base_rule.tracked_changes)
        base_rule.track_change(old_version, new_version)
        self.assertEqual([], base_rule.tracked_changes)


if __name__ == '__main__':
    unittest.main()

