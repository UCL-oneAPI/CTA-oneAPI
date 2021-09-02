import unittest

from auto_editor.Fix1049Rule import Fix1049Rule
from auto_editor.StructuredProjectSource import StructuredProjectSource
from testing_support.BaseTest import BaseTest


class TestFix1049Rule(BaseTest):
    @property
    def test_project(self):
        path = self.get_full_test_path("unit_testing_data/1049_testing")
        return StructuredProjectSource(path)

    def test_runRule_warningWithRange_warningResolved(self):
        path_to_file = '1049_inline_range/1049_with_range.dp.cpp'
        new_project = Fix1049Rule().run_rule(project=self.test_project, warning_first_line=3,
                                             warning_last_line=7, file_path=path_to_file)
        lines_in_file = new_project.paths_to_lines[path_to_file]
        self.assertEqual(22, len(lines_in_file))

        has_global_range_declaration = "auto dpct_global_range = " in lines_in_file[4].code
        self.assertTrue(has_global_range_declaration)

    def test_runRule_warningWithNamedRange_warningResolved(self):
        path_to_file = '1049_declared_range/1049_named_range.dp.cpp'
        new_project = Fix1049Rule().run_rule(project=self.test_project, warning_first_line=3,
                                             warning_last_line=7, file_path=path_to_file)
        lines_in_file = new_project.paths_to_lines[path_to_file]
        self.assertEqual(22, len(lines_in_file))

        has_global_range_declaration = "auto dpct_global_range = " in lines_in_file[4].code
        self.assertTrue(has_global_range_declaration)

    def test_runRule_warningWithNamedRangeSingleLine_warningResolved(self):
        path_to_file = '1049_declared_range/1049_named_range_single_line.dp.cpp'
        new_project = Fix1049Rule().run_rule(project=self.test_project, warning_first_line=0,
                                             warning_last_line=4, file_path=path_to_file)
        lines_in_file = new_project.paths_to_lines[path_to_file]
        self.assertEqual(21, len(lines_in_file))

        has_global_range_declaration = "auto dpct_global_range = " in lines_in_file[7].code
        self.assertTrue(has_global_range_declaration)


if __name__ == '__main__':
    unittest.main()
