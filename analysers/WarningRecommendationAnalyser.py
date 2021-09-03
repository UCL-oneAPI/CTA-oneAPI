from analysers.WarningAnalyser import WarningAnalyser
from auto_editor.StructuredProjectSource_Recommendation import StructuredProjectSource_Recommendation
from enums import RecommendationItem
from typing import List


class WarningRecommendationAnalyser(WarningAnalyser):
    """
    Basically, the same as the pre-analyzer,
    plus the ability to also detect and count new CTA warnings/recommendations.
    We currently don't have any of these,
    so I recommend working with a 'dummy' string here.
    E.g. for the ticket you can assume that all CTA warnings/recommendations begin with "CTA<some-number>: "
    """

    def count_warnings_numbers(self, warning_code, cta_number, dpct_number):
        if 'CTA' in warning_code:
            cta_number += 1
        elif 'DPCT' in warning_code:
            dpct_number += 1
        return cta_number, dpct_number

    def get_all_recommendation(self) -> List[RecommendationItem]:
        project = StructuredProjectSource_Recommendation(self.project_root_path)
        recommendations_dict = project.recommendations_dict
        all_recommendations = []
        all_codes = {}
        all_ids = {}

        for name, line_items in project.paths_to_lines.items():
            for i in line_items:
                all_codes.setdefault(name, []).append(i.code)
                all_ids.setdefault(name, []).append(i.id)

        for k, v in recommendations_dict.items():
            for info in v:
                first_line_id = info[0]
                last_line_id = info[1]
                file_path = info[2]
                path = '/' + file_path
                if file_path in all_ids.keys():
                    codes = all_codes[file_path]
                    ids = all_ids[file_path]
                    first_line = self.get_first_line_num(first_line_id, codes, ids)
                    message = self.get_warning_message(first_line, last_line_id, codes, ids)
                    warning = RecommendationItem(project_name=self.project_root_path.stem,
                                                 recommendation_code=k,
                                                 file_path=path,
                                                 message=message,
                                                 line=first_line)
                    all_recommendations.append(warning)

        return all_recommendations
