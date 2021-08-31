import unittest

from analysers.WarningAnalyser import WarningAnalyser
from testing_support.BaseIntegrationTest import BaseIntegrationTest


class TestWarningAnalyserIntegration(BaseIntegrationTest):

    def test_getAllWarnings_dpctProjectWithWarning_warningExtracted(self):
        warning_analyser = WarningAnalyser(self.dpct_root)
        warnings = warning_analyser.get_all_warnings()

        self.assertEqual(len(warnings), 22)
        self.assertEqual(warnings[0].project_name, 'test_project')
        self.assertEqual(warnings[0].warning_code, 'DPCT1111')
        self.assertEqual(warnings[0].file_path, '/kernel_wrapper2.dp.cpp')
        self.assertEqual(warnings[0].message,
                         "DPCT1111:3: The workgroup size passed to the SYCL kernel may exceed the limit.\n"
                         "To get the device limit, query info::device::max_work_group_size. Adjust the\n"
                         "workgroup size if needed.")  # @Yifei I hope this is correct with the "\n" and spacing,
        # otherwise feel free to make changes
        self.assertEqual(warnings[0].line, 127)


if __name__ == '__main__':
    unittest.main()
