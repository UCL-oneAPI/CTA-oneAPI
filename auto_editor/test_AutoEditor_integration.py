import os
import unittest

from auto_editor.AutoEditor import AutoEditor
from enums import DiffOperationEnum, ChangeTypeEnum
from testing_support.BaseIntegrationTest import BaseIntegrationTest


class TestAutoEditorIntegration(BaseIntegrationTest):
    def test_makeChanges_dpctProjectWithWarnings_warningsFixed(self):
        editor = AutoEditor(dpct_version_root=self.dpct_root,
                            cta_version_root=self.destination_root)
        changes = editor.make_changes()

        self.assertEqual(len(changes), 6)
        for i in range(5):
            self.assertEqual(changes[i].diff_operation, DiffOperationEnum.delete)

        self.assertEqual(changes[5].diff_operation, DiffOperationEnum.add)

        for change in changes:
            self.assertEqual(change.change_type, ChangeTypeEnum.recommendation)


if __name__ == '__main__':
    unittest.main()
