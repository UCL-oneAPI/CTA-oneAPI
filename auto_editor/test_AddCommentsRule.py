import unittest

from auto_editor.Fix1049Rule import Fix1049Rule
from auto_editor.StructuredProjectSource import StructuredProjectSource
from testing_support.BaseTest import BaseTest
from auto_editor.AddCommentsRule import AddCommentsRule
from pathlib import Path
from auto_editor.AutoEditor import AutoEditor
import os
class TestFix1049Rule(BaseTest):
    @property
    def test_project(self):
        path = self.get_full_test_path("unit_testing_data/AddComments_testing")
        return StructuredProjectSource(path)

    def test_runRule_warningWithRange_warningResolved(self):
        path_to_file = 'comments_range.dp.cpp'
        new_project = AddCommentsRule().run_rule(project=self.test_project, warning_first_line=3,
                                             warning_last_line=7, file_path=path_to_file)
        cta_root = Path(__file__).parent.parent.resolve()
        path_to_new_root = Path.joinpath(cta_root, 'testing_support', 'unit_testing_data', 'AddComments_testing', 'result_files')

        if os.path.exists(path_to_new_root):
            for f in os.listdir(path_to_new_root):
                os.remove(os.path.join(path_to_new_root, f))
            os.rmdir(os.path.join(path_to_new_root))
        os.mkdir(os.path.join(path_to_new_root))
        editor = AutoEditor(dpct_version_root=Path.joinpath(cta_root, 'testing_support', 'unit_testing_data', 'AddComments_testing'), cta_version_root=path_to_new_root)
        changes = editor.make_changes()
        self.assertEqual(6, len(changes))



if __name__ == '__main__':
    unittest.main()
