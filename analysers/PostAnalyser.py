from analysers.BaseAnalyser import BaseAnalyser

from auto_editor.StructuredProjectSource import StructuredProjectSource
from auto_editor.StructuredProjectSource_Recommendation import StructuredProjectSource_Recommendation
from enums import WarningItem, RecommendationItem
from typing import List


class PostAnalyser(BaseAnalyser):
    """
    Basically, the same as the pre-analyzer,
    plus the ability to also detect and count new CTA warnings/recommendations.
    We currently don't have any of these,
    so I recommend working with a 'dummy' string here.
    E.g. for the ticket you can assume that all CTA warnings/recommendations begin with "CTA<some-number>: "
    """

    def get_all_warnings(self) -> List[WarningItem]:
        '''
        This creates the data for the report of dpct warnings.
        It analyses the project in self.project_root_path.
        :return: list of named tuples WarningItem, one WarningItem for each warning in the project
        '''

        project = StructuredProjectSource(self.project_root_path)
        warnings_dict = project.dpct_warnings_dict
        all_warnings = []
        all_codes = {}
        all_ids = {}

        for name, line_item in project.paths_to_lines.items():
            for i in line_item:
                all_codes.setdefault(name, []).append(i.code)
                all_ids.setdefault(name, []).append(i.id)

        for k, v in warnings_dict.items():
            for info in v:
                path = '/' + info[2]
                if info[2] in all_ids.keys():
                    codes = all_codes[info[2]]
                    ids = all_ids[info[2]]
                    first_line = self.get_first_line_num(info[0], codes, ids)
                    message = self.get_warning_message(first_line, info[1], codes, ids)
                    # cta_number, dpct_number = self.count_warnings_numbers(k,cta_number,dpct_number)
                    warning = WarningItem(project_name=self.project_root_path.stem,
                                          warning_code=k,
                                          file_path=path,
                                          message=message,
                                          line=first_line)
                    all_warnings.append(warning)
        return all_warnings

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

        for name, line_item in project.paths_to_lines.items():
            for i in line_item:
                all_codes.setdefault(name, []).append(i.code)
                all_ids.setdefault(name, []).append(i.id)

        for k, v in recommendations_dict.items():
            for info in v:
                path = '/' + info[2]
                if info[2] in all_ids.keys():
                    codes = all_codes[info[2]]
                    ids = all_ids[info[2]]
                    first_line = self.get_first_line_num(info[0], codes, ids)
                    message = self.get_warning_message(first_line, info[1], codes, ids)
                    warning = RecommendationItem(project_name=self.project_root_path.stem,
                                                 recommendation_code=k,
                                                 file_path=path,
                                                 message=message,
                                                 line=first_line)
                    all_recommendations.append(warning)


        return all_recommendations
