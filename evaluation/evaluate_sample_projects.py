import argparse
import os
from pathlib import Path

import pandas as pd

from command_handler import run_cta
from report_presentation.Presenter import Presenter


def evaluate_samples(projects_root, report_path):
    all_initial_warnings = []
    all_final_warnings = []
    all_cta_recommendations = []
    all_changes = []
    all_projects = os.listdir(projects_root)

    # run cta on all projects
    for project_name in all_projects:
        print('project_name:', project_name)
        path = projects_root + '/' + project_name
        dpct_root = path + '/dpcpp'  # expected to be provided in each project
        destination_dir = path + '/cta-version'
        project_report_dir = path + '/cta-report'
        cta_instance = run_cta(dpct_root, destination_dir, project_report_dir)

        all_initial_warnings = augment_and_extend(cta_instance.initial_warnings, project_name, all_initial_warnings)
        all_final_warnings = augment_and_extend(cta_instance.final_warnings, project_name, all_final_warnings)
        all_cta_recommendations = augment_and_extend(cta_instance.cta_recommendations, project_name,
                                                     all_cta_recommendations)
        all_changes = augment_and_extend(cta_instance.changes, project_name, all_changes)

    # create accumulated csvs
    cta_tool_root = Path(__file__).parent.parent.resolve()
    csv_root = cta_tool_root / report_path / 'raw_data'
    if not os.path.exists(csv_root):
        os.mkdir(csv_root)
    pd.DataFrame(all_initial_warnings).to_csv(csv_root / 'all_initial_warnings.csv')
    pd.DataFrame(all_final_warnings).to_csv(csv_root / 'all_final_warnings.csv')
    pd.DataFrame(all_cta_recommendations).to_csv(csv_root / 'all_cta_recommendations.csv')
    pd.DataFrame(all_changes).to_csv(csv_root / 'all_changes.csv')

    # create interactive report
    presenter = Presenter(cta_tool_root / report_path,
                          '',
                          # dpct and destination paths cannot be provided since inside the respective project paths.
                          '',  # presenter hence has broken links, but sufficient for evaluation
                          all_initial_warnings,
                          all_cta_recommendations,
                          all_final_warnings,
                          all_changes)
    presenter.generate_ui_files()

    print('All projects:', len(all_projects))


def augment_and_extend(items: list, project_name: str, all_list: list):
    for item in items:
        new_file_path = project_name + '/...' + item.file_path
        new_item = item._replace(file_path=new_file_path)
        all_list.append(new_item)
    return all_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyse group of projects')

    parser.add_argument('--projects-root-path', type=str, action='store',
                        help='this is the root path where all projects should be in.'
                             'This program expects that each project contains'
                             ' a subfolder "dpct-version", which contains the'
                             ' source code with dpct warnings')
    parser.add_argument('--aggregated-report-path', type=str, action='store',
                        help='this is the path for the overall report generated by CTA.'
                             ' Per-project reports will be added as a new "report" folder in each project,'
                             ' but the aggregated report will be retrievable from this root.')
    args = parser.parse_args()

    if not args.projects_root_path or not os.path.exists(args.projects_root_path):
        raise Exception("Please provide valid --projects-root-path.")

    if not args.aggregated_report_path:
        raise Exception("Please provide --aggregated-report-path.")
    else:
        if not os.path.exists(args.aggregated_report_path):
            os.mkdir(args.aggregated_report_path)

    evaluate_samples(args.projects_root_path, args.aggregated_report_path)