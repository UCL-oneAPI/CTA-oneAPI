from analysers.BaseAnalyser import BaseAnalyser
from auto_editor.StructuredProjectSource import StructuredProjectSource
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
        project = StructuredProjectSource(self.project_root_path)
        warnings_dict = project.dpct_warnings_dict
        all_warnings = []
        codes = []
        ids = []
        cta_number,dpct_number = 0

        for i in project.paths_to_lines.values():
            for j in i:
                codes.append(j.code)
                ids.append(j.id)

        for k, v in warnings_dict.items():
            for info in v:
                path = '/' + info[2]
                first_line = self.get_first_line_num(info[0], codes, ids)
                message = self.get_warning_message(first_line, info[1], codes, ids)
                cta_number, dpct_number = self.count_warnings_numbers(k,cta_number,dpct_number)
                warning = WarningItem(project_name=self.project_root_path.stem,
                                      warning_code=k,
                                      file_path=path,
                                      message=message,
                                      line=first_line)
                all_warnings.append(warning)
        return all_warnings,cta_number, dpct_number


    def count_warnings_numbers(self, warning_code,cta_number,dpct_number):
        if 'CTA' in warning_code:
            cta_number += 1
        elif 'DPCT' in warning_code:
            dpct_number += 1
        return cta_number,dpct_number

    def get_all_recommendation(self) -> List[RecommendationItem]:
        project = StructuredProjectSource(self.project_root_path)
        #
        # # loop through every line in project
        # recommendation_message,line = "",0
        # all_recommendations = []
        # for file_name, warnings in project.paths_to_lines.items():
        #     start_flag = False
        #     for lineItem in warnings:
        #         code = lineItem.code
        #         if "CTA" in code:
        #             start_flag = True
        #             recommendation_message += str(code)
        #         if start_flag == True:
        #             recommendation_message += str(code)
        #             if "*/" in code:
        #                 recommendation_item = RecommendationItem(project_name=self.project_root_path.stem,
        #                                       recommendation_code=k,
        #                                       file_path=path,
        #                                       message=recommendation_message,
        #                                       line=first_line)
        #                 recommendation_message = ""
        #                 start_flag = False
        #                 all_recommendations.append(recommendation_item)
        # return all_recommendations

