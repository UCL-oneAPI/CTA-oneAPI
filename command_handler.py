from CTA_Instance import CTA_Instance
import argparse
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
    filenames = os.listdir(dpct_project_path)
    state_cpp = False
    for filename in filenames:
        if filename.endswith('.cpp') is True:
            state_cpp = True

    if not state_cpp:
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


if __name__ == '__main__':
    # implement of command line interface
    parser = argparse.ArgumentParser(description='Welcome to use Code Translation Assistant(CTA) for Intel oneAPI \n'
                                                 'We provide you several modes to use CTA which can help you easily '
                                                 'adapt the code generated by Intel oneAPI \n'
                                                 'To use CTA, you need to use command:')
    parser.add_argument('--mode', type=str, help="This is used to select the mode you want CTA to run on",
                        choices=['default', 'report_only'], )
    # parser.add_argument('-i', '--input', type=str, action='store', nargs=3)
    parser.add_argument('--project-path', type=str, action='store',
                        help='this is the project path you want to run CTA on ')
    parser.add_argument('--destination-path', type=str, action='store', help=' this is the path for the output files')
    parser.add_argument('--report-path', type=str, action='store', help='this is the path for report generated by CTA')
    parser.version = 'CTA 1.0.0'
    parser.add_argument('--version', action='version')
    args = parser.parse_args()

    validate_check_result = validate_paths(args.project_path,args.destination_path)
    if validate_check_result is True:
        if args.mode == 'default':
            run_cta(args.project_path, args.destination_path, args.report_path)

        if args.mode == 'report_only':
            run_cta(args.project_path, args.destination_path, args.report_path,is_report_only=True)
    else:
        print(validate_check_result)


