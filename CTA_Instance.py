import os
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
        self.cta_recommendations = []
        self.changes = []

    def run_pre_analyzer(self):
        '''
        populate self.initial_warnings
        '''
        pre_analyser = PreAnalyser(self.dpct_version_root)
        self.initial_warnings = pre_analyser.get_all_warnings()
        # print('initial: ',len(self.initial_warnings))

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
        self.final_warnings = post_analyser.get_all_warnings()
        self.cta_recommendations = post_analyser.get_all_recommendation()

    def save_to_csvs(self):
        '''
        Store initial_warnings, final_warnings and changes as separate csvs,
        so that they can be inspected after the run.
        :return: path to newly generated folder where these csvs are stored (next to presentation folder)
        '''
        root = self.report_root + "/raw_data"
        folder = os.path.exists(root)
        if not folder:
            os.mkdir(root)
        pd.DataFrame(self.initial_warnings).to_csv(root + '/pre-analyzer.csv')
        pd.DataFrame(self.final_warnings).to_csv(root + '/post_analyzer.csv')
        pd.DataFrame(self.changes).to_csv(root + '/changes.csv')
        pd.DataFrame(self.cta_recommendations).to_csv(root + '/cta_recommendations.csv')

    def create_report_presentation(self):
        '''
        create files for report
        '''

        presenter = Presenter(self.report_root, self.dpct_version_root, self.cta_version_root, self.initial_warnings,
                              self.cta_recommendations, self.final_warnings, self.changes)

        presenter.generate_ui_files()