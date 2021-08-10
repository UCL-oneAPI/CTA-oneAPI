import os
from pathlib import Path

from auto_editor.AutoEditor import AutoEditor
from auto_editor.Fix1003Rule import Fix1003Rule
from auto_editor.StructuredProjectSource import StructuredProjectSource


def call_run_rule():
    local_path_to_file = 'cluster.dp.cpp'
    #local_path_to_file = 'kernel_wrapper2.dp.cpp'
    cta_root = Path(__file__).parent.parent.resolve()
    path_to_dpct_root = Path.joinpath(cta_root, 'auto_editor', 'sample_data', 'test_project')
    path_to_new_root = Path.joinpath(cta_root, 'auto_editor', 'sample_data', 'destination_dir')

    if os.path.exists(path_to_new_root):
        for f in os.listdir(path_to_new_root):
            os.remove(os.path.join(path_to_new_root, f))
        os.rmdir(os.path.join(path_to_new_root))
    os.mkdir(os.path.join(path_to_new_root))

    rule = Fix1003Rule()
    project = StructuredProjectSource(path_to_dpct_root)
    #project = rule.run_rule(project=project, warning_first_line=117,
    #                        warning_last_line=120, file_path=local_path_to_file)

    # one line warning code
    project = rule.run_rule(project=project, warning_first_line=330,
                            warning_last_line=333, file_path=local_path_to_file)
    print("---------------------------------------------------------------------------")

    #multiple line warning code
    project = rule.run_rule(project=project, warning_first_line=335,
                            warning_last_line=338, file_path=local_path_to_file)

    print("---------------------------------------------------------------------------")

    # test prefix
    project = rule.run_rule(project=project, warning_first_line=411,
                            warning_last_line=414, file_path=local_path_to_file)

    create_new_version(project, new_root=path_to_new_root)


def create_new_version(project, new_root):
    # this just saves the version in the new_root path, so it's easier to look at it.
    editor = AutoEditor(dpct_version_root=Path(''), cta_version_root=new_root)
    editor.save_new_version(project)


if __name__ == '__main__':
    call_run_rule()
