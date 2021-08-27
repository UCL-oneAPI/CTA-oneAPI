import unittest

from auto_editor.Fix1003Rule import Fix1003Rule
from auto_editor.StructuredProjectSource import StructuredProjectSource
from testing_support.BaseTest import BaseTest


class Test_Fix1003Rule(BaseTest):
    @property
    def test_project(self):
        path = self.get_full_test_path("unit_testing_data/1003_testing")
        return StructuredProjectSource(path)

    def test_runRule_warningWithRange_warningResolved(self):
        path_to_file = '1003_inline_range/1003_with_range.dp.cpp'
        new_project = Fix1003Rule().run_rule(project=self.test_project, warning_first_line=1,
                                             warning_last_line=4, file_path=path_to_file)
        lines_in_file = new_project.paths_to_lines[path_to_file]
        self.assertEqual(3, len(lines_in_file))
        #
        has_global_range_declaration = "c->Rinv = (float *)sycl::malloc_device(sizeof(float) * num_dimensions *num_dimensions * num_clusters,q_ct1);" in lines_in_file[1].code
        self.assertTrue(has_global_range_declaration)

    def test_runRule_warningWithNamedRange_warningResolved(self):
        path_to_file = '1003_declared_range/1003_named_range.dp.cpp'
        new_project = Fix1003Rule().run_rule(project=self.test_project, warning_first_line=2,
                                             warning_last_line=5, file_path=path_to_file)
        lines_in_file = new_project.paths_to_lines[path_to_file]
        self.assertEqual(6, len(lines_in_file))
        #
        has_global_range_declaration = "c->Rinv = (float *)sycl::malloc_device(sizeof(float) * num_dimensions *num_dimensions * num_clusters,q_ct1);" in lines_in_file[2].code
        self.assertTrue(has_global_range_declaration)


if __name__ == '__main__':
    unittest.main()
