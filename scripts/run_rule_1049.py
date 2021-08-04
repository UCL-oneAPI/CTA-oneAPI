from auto_editor.AddCommentsTestRule import AddCommentsTestRule
from auto_editor.AutoEditor import AutoEditor
from auto_editor.StructuredProjectSource import StructuredProjectSource


def call_run_rule():
    local_path_to_file = 'kernel_wrapper2.dp.cpp'
    path_to_dpct_root = '../auto_editor/sample_data/test_project'
    path_to_new_root = '../auto_editor/sample_data/destination_dir'

    rule = AddCommentsTestRule()
    project = StructuredProjectSource(path_to_dpct_root)
    project = rule.run_rule(project=project, warning_first_line=125,
                            warning_last_line=129, file_path=local_path_to_file)

    create_new_version(project, new_root=path_to_new_root)


def create_new_version(project, new_root):
    # this just saves the version in the new_root path, so it's easier to look at it.
    editor = AutoEditor(dpct_version_root='', cta_version_root=new_root)
    editor.save_new_version(project)


if __name__ == '__main__':
    call_run_rule()
