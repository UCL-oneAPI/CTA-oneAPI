from pathlib import Path

from analysers.PostAnalyser import PostAnalyser
from analysers.PreAnalyser import PreAnalyser
from auto_editor.AutoEditor import AutoEditor
from report_presentation.Presenter import Presenter

import pandas as pd


class CTA_Instance:
    '''
    the same CTA_Instance is used throughout a single run of CTA.
    Data created/used in different components can be stored here.
    '''

    def __init__(self, dpct_version_root, cta_version_root, report_root):
        cta_tool_root = Path(__file__).parent.resolve()
        self.dpct_version_root = cta_tool_root / dpct_version_root
        self.cta_version_root = cta_tool_root / cta_version_root
        self.report_root = report_root
        self.initial_warnings = []
        self.final_warnings = []
        self.changes = []

    def run_pre_analyzer(self):
        '''
        populate self.initial_warnings
        '''
        pre_analyser = PreAnalyser(self.dpct_version_root)
        self.initial_warnings = pre_analyser.get_all_warnings()

    def run_editor(self):
        '''
        creates an edited version of the dpct version in destination_root.
        Changes are documented in self.changes
        '''
        editor = AutoEditor(self.dpct_version_root, self.cta_version_root)
        documented_changes = editor.make_changes()
        self.changes = documented_changes

    def run_post_analyzer(self):
        '''
        populate self.final_warnings based on analysis of final version
        '''
        post_analyser = PostAnalyser(self.cta_version_root)
        self.initial_warnings = post_analyser.get_all_warnings()

    def save_to_csvs(self):
        '''
        Store initial_warnings, final_warnings and changes as separate csvs,
        so that they can be inspected after the run.
        :return: path to newly generated folder where these csvs are stored (next to presentation folder)
        '''
        pd.DataFrame(self.initial_warnings).to_csv('pre-analyzer.csv')
        pd.DataFrame(self.final_warnings).to_csv('post_analyzer.csv')
        pd.DataFrame(self.changes).to_csv('changes.csv')

    def create_report_presentation(self):
        '''
        create files for report
        '''
        presenter = Presenter(self.report_root, self.initial_warnings, self.final_warnings, self.changes)
        presenter.generate_ui_files()

if __name__ == '__main__':
    cta = CTA_Instance(r"C:\Users\lenovo\Desktop\CTA-oneAPI\auto_editor\sample_data\test_project",
                       r"C:\Users\lenovo\Desktop\CTA-oneAPI\auto_editor\sample_data\destination_dir\kernel_wrapper2.dp.cpp",
                       r"C:\Users\lenovo\Desktop\CTA-oneAPI\auto_editor\sample_data")
    cta.run_pre_analyzer()
    cta.save_to_csvs()
