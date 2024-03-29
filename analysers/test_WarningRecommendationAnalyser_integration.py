import unittest

from analysers.WarningRecommendationAnalyser import WarningRecommendationAnalyser
from testing_support.BaseIntegrationTest import BaseIntegrationTest


class TestWarningRecommendationAnalyserIntegration(BaseIntegrationTest):

    def test_getAllWarnings_dpctProjectWithWarning_warningExtracted(self):
        p = self.get_full_test_path("integration_testing_data/post_analyzer_testing_data")
        print("cta_root:", p)
        warning_recommendation_analyser = WarningRecommendationAnalyser(p)
        final_warnings = warning_recommendation_analyser.get_all_warnings()
        recommendations = warning_recommendation_analyser.get_all_recommendation()
        print(recommendations)


        self.assertEqual(len(recommendations), 2)
        self.assertEqual(recommendations[0].project_name, 'post_analyzer_testing_data')
        self.assertEqual(recommendations[0].recommendation_code, 'CTA1003')
        self.assertEqual(recommendations[0].file_path, '/cluster.dp.cpp')
        self.assertEqual(recommendations[0].message,'CTA1003:1: This is the test recommendation for CTA system.')

        #self.assertEqual(recommendations[0].line, 247)
        pass


if __name__ == '__main__':
    unittest.main()
