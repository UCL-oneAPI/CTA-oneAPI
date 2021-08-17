import unittest

from analysers.PostAnalyser import PostAnalyser
from testing_support.BaseIntegrationTest import BaseIntegrationTest


class TestPreAnalyzerIntegration(BaseIntegrationTest):

    def test_getAllWarnings_dpctProjectWithWarning_warningExtracted(self):
        post_analyser = PostAnalyser(self.dpct_root)
        recommendations = post_analyser.get_all_recommendation()
        print(recommendations)

        self.assertEqual(len(recommendations), 24)
        self.assertEqual(recommendations[0].project_name, 'test_project')
        self.assertEqual(recommendations[0].recommendation_code, 'DPCT1111')
        self.assertEqual(recommendations[0].file_path, '/kernel_wrapper2.dp.cpp')
        self.assertEqual(recommendations[0].message,
                         "DPCT1111:3: The workgroup size passed to the SYCL kernel may exceed the limit.\n"
                         "To get the device limit, query info::device::max_work_group_size. Adjust the\n"
                         "workgroup size if needed.")  # @Yifei I hope this is correct with the "\n" and spacing,
        # otherwise feel free to make changes
        self.assertEqual(recommendations[0].line, 127)


if __name__ == '__main__':
    unittest.main()
