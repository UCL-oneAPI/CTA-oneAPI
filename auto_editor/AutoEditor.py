from pathlib import Path
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
        for path, code_lines in project.paths_to_lines.items():
            full_path = self.cta_version_root / path
            Path(full_path.parent).mkdir(parents=True, exist_ok=True)
            with open(full_path, 'a+') as f:
                for line in code_lines:
                    f.write(line.code)
