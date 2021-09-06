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

        lines_in_file = new_project.paths_to_lines[path_to_file]
        self.assertEqual(15, len(lines_in_file))

        has_global_range_declaration = "CTA1065:3: CTA recommended to ignore this warning." in lines_in_file[3].code
        self.assertTrue(has_global_range_declaration)

if __name__ == '__main__':
    unittest.main()
