import os
from pathlib import Path
from shutil import copyfile
from typing import List

from auto_editor.StructuredProjectSource import StructuredProjectSource
from constants import RULES_TO_DESCRIPTIONS
from enums import CodeChange


class AutoEditor:
    def __init__(self, dpct_version_root: Path, cta_version_root: Path):
        self.dpct_version_root = dpct_version_root
        self.cta_version_root = cta_version_root

    def make_changes(self) -> List[CodeChange]:
        '''
        apply the different rules to create the new version in self.cta_version_root.
        changes are documented as they are made and returned in documented_changes

        :return:
        documented_changes: list of changes. Format: namedTuple AppliedChange
        '''

        all_documented_changes = []
        project = StructuredProjectSource(self.dpct_version_root)

        for rule in RULES_TO_DESCRIPTIONS:
            rule_instance = rule()
            rule_instance.initiate_run(project)
            changes = rule_instance.get_tracked_changes()
            for change in changes:
                all_documented_changes.append(change)

        self.save_new_version(project)
        return all_documented_changes

    def save_new_version(self, project: StructuredProjectSource):
        self.copy_non_dpct_files(project)
        for path, code_lines in project.paths_to_lines.items():
            full_path = self.cta_version_root / path
            Path(full_path.parent).mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w+') as f:
                for line in code_lines:
                    f.write(line.code)

    def copy_non_dpct_files(self, project):
        '''
        CTA version should also contain all other files, e.g. '.c','.yaml', or '.h',
        so this method copies them into the new directory
        '''
        non_dpct_relevant_paths = self.get_all_non_dpct_paths(project)
        for path in non_dpct_relevant_paths:
            full_src_path = self.dpct_version_root / path
            if os.path.isdir(full_src_path):
                continue

            full_dest_path = self.cta_version_root / path
            Path(full_dest_path.parent).mkdir(parents=True, exist_ok=True)
            copyfile(full_src_path, full_dest_path)

    def get_all_non_dpct_paths(self, project) -> List[str]:
        '''
        Find all non-dpct files in dpct root and its subfolders
        :return: list with paths to all files inside directory at self.dpct_version_root
        '''
        all_dpct_files = []
        paths = []
        project_path = str(self.dpct_version_root.stem)
        root_index = 0

        all_dpct_files.extend(self.dpct_version_root.rglob('*'))
        for file in all_dpct_files:
            path_parts = file.parts
            if project_path in path_parts:
                root_index = path_parts.index(project_path)
            dpct_path = '/'.join(path_parts[root_index + 1:])
            if dpct_path not in project.paths_to_lines:
                paths.append(dpct_path)

        return paths
