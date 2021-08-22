from auto_editor.StructuredProjectSource_Recommendation import StructuredProjectSource_Recommendation
from pathlib import Path


if __name__ == '__main__':

    cta_root = Path(__file__).parent.parent.resolve()
    path_to_dpct_root = Path.joinpath(cta_root, 'auto_editor', 'sample_data', 'destination_dir')

    project = StructuredProjectSource_Recommendation(path_to_dpct_root)
    print(project.get_all_recommendations())