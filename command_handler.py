from CTA_Instance import CTA_Instance
import argparse
import os
import os.path


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
    if os.path.exists(dpct_project_path) is False:
        raise Exception(dpct_project_path + " does not exist.")

    filenames = []
    for root, dirs, files in os.walk(dpct_project_path):
        filenames.extend(files)
    state_cpp = False
    for filename in filenames:
        if filename.endswith('.cpp') or filename.endswith('.hpp'):
            state_cpp = True

    if not state_cpp:
        raise Exception(dpct_project_path + " does not contain the cpp or hpp file.")
    elif os.path.exists(destination_path) is False:
        raise Exception(destination_path + " does not exist")
    elif os.path.isdir(destination_path) is False:
        raise Exception(destination_path + " is not a folder.")
    elif os.listdir(destination_path):
        raise Exception(destination_path + " is not empty.")


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

    des = ""
    if args.destination_path == None:
        des = ""
    else:
        if os.path.exists(args.destination_path):
            des = '/'+str(args.destination_path)
        else:
            os.mkdir(args.destination_path)  # make directory

    output_folder_path = (str(os.getcwd()) + str(des)+'\outputs').replace('\\','/')
    if os.path.exists(output_folder_path):
        pass
    else:
        os.mkdir(output_folder_path)  # make directory
    # print(output_folder_path)
    validate_check_result = validate_paths(args.project_path,
                                           output_folder_path)  # get validate path checking result
    if validate_check_result is True:
        if args.mode == 'default':
            run_cta(args.project_path, args.destination_path, args.report_path)

        if args.mode == 'report_only':
            run_cta(args.project_path, args.destination_path, args.report_path, is_report_only=True)
    else:
        print(validate_check_result)
