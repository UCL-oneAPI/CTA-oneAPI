import os
import unittest

from auto_editor.AutoEditor import AutoEditor
from enums import DiffOperationEnum, ChangeTypeEnum


class TestAutoEditorIntegration(unittest.TestCase):
    def destination_path(self):
        return '../auto_editor/integration_testing_data/destination_dir'

    def test_makeChanges_dpctProjectWithWarnings_warningsFixed(self):
        dpct_root = '../auto_editor/integration_testing_data/test_project'
        new_root = self.destination_path()

        editor = AutoEditor(dpct_version_root=dpct_root, cta_version_root=new_root)
        changes = editor.make_changes()

        self.assertEqual(len(changes), 6)
        for i in range(5):
            self.assertEqual(changes[i].diff_operation, DiffOperationEnum.delete)

        self.assertEqual(changes[5].diff_operation, DiffOperationEnum.add)

        for change in changes:
            self.assertEqual(change.change_type, ChangeTypeEnum.recommendation)

    def tearDown(self) -> None:
        for f in os.listdir(self.destination_path()):
            os.remove(os.path.join(self.destination_path(), f))

if __name__ == '__main__':
    unittest.main()
