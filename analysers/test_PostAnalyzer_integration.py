import unittest

from analysers.PostAnalyser import PostAnalyser
from testing_support.BaseIntegrationTest import BaseIntegrationTest
from auto_editor import StructuredProjectSource_Recommendation
from pathlib import Path

class TestPreAnalyzerIntegration(BaseIntegrationTest):

    def test_getAllWarnings_dpctProjectWithWarning_warningExtracted(self):


        cta_root = Path(__file__).parent.parent.resolve()
        p = Path.joinpath(cta_root, 'auto_editor', 'sample_data', 'destination_dir')
        print("cta_root:",p)
        post_analyser = PostAnalyser(p)
        final_warnings = post_analyser.get_all_warnings()
        recommendations = post_analyser.get_all_recommendation()
        print(recommendations)
        self.assertEqual(len(final_warnings), 57)
        self.assertEqual(final_warnings[0].project_name, 'destination_dir')
        self.assertEqual(final_warnings[0].warning_code, 'DPCT1003')
        self.assertEqual(final_warnings[0].file_path, '/cluster.dp.cpp')
        self.assertEqual(final_warnings[0].message, "DPCT1003:28: Migrated API does not return error code. (*, 0) is inserted. You\n"
                                                    "may need to rewrite this code.")

        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations[0].project_name, 'destination_dir')
        self.assertEqual(recommendations[0].recommendation_code, 'CTA1065')
        self.assertEqual(recommendations[0].file_path, '/kernels.dp.cpp')
        self.assertEqual(recommendations[0].message,"CTA1065:0: CTA recommended to ignore this warning.\n"
                                                    "but you can also consider replacing 'item_ct1.barrier();'\n"
                                                    "with 'item_ct1.barrier(sycl::access::fence_space::local_space);'\n"
                                                    "to have have better performance if the kernel function\n"
                                                    "has no memory accesses in the global memory.")
        #self.assertEqual(recommendations[0].line, 247)
        pass


if __name__ == '__main__':
    unittest.main()
