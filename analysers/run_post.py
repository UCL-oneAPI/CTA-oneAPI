from auto_editor.StructuredProjectSource_Recommendation import StructuredProjectSource_Recommendation
from auto_editor.StructuredProjectSource_Recommendation import StructuredProjectSource
from pathlib import Path

def run():
    cta_root = Path(__file__).parent.parent.resolve()
    p = Path.joinpath(cta_root, 'auto_editor', 'sample_data', 'destination_dir')
    t = StructuredProjectSource_Recommendation(p)
    # t = StructuredProjectSource(p)
    print(t)


run()