from CTA_Instance import CTA_Instance
import os

# This defines the CLI and handles user commands.
# Todo Zhongyuan: add CLI implementation


def run_cta(dpct_project_path, destination_path, report_path, is_report_only=False):
    validate_paths(dpct_project_path, destination_path)
    cta_instance = CTA_Instance(dpct_project_path, destination_path, report_path)
    cta_instance.run_pre_analyzer()

    if not is_report_only:
        cta_instance.run_editor()
        cta_instance.run_post_analyzer()

    cta_instance.create_report_presentation()
    cta_instance.save_to_csvs()


def validate_paths(dpct_project_path, destination_path):
    '''
    :param dpct_project_path:
    :param destination_path:

    generates exceptions if directory of destination_path is not empty
    or if dpct_project_path directory contains no (nested) .dp.cpp or .dp.h files
    '''

    if dpct_project_path.endswith('.cpp') is False:
        r = "The path does not contain the cpp file."
        return r
    elif os.path.exists(destination_path) is False:
        r = "This path does not exist."
        return r
    elif os.path.isdir(destination_path) is False:
        r = "This is not a folder."
        return r
    elif os.listdir(destination_path):
        r = "This folder is not empty."
        return r
    else:
        print("Works!")
        return True
