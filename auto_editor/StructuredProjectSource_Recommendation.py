from auto_editor.StructuredProjectSource import StructuredProjectSource
from enums import RecommendationLocation


class StructuredProjectSource_Recommendation(StructuredProjectSource):
    def __init__(self):
        self.recommendations_dict = self.get_all_recommendations()

    def get_all_recommendations(self):
        recommendations_dict = {}
        for file_path, code_lines in self.paths_to_lines.items():
            for i in range(len(code_lines)):
                line_item = code_lines[i]
                recommendation_code = line_item.get_cta_recommendation()
                if recommendation_code:
                    first_line = self.get_first_warning_line(i, code_lines)
                    last_line = self.get_last_warning_line(i, code_lines)

                    if recommendation_code not in recommendations_dict:
                        recommendations_dict[recommendation_code] = []

                    recommendations_dict[recommendation_code].append(
                        RecommendationLocation(first_line.id, last_line.id, file_path)
                    )

        return recommendations_dict
