from typing import List

from constants import RULES_TO_DESCRIPTIONS
from enums import CodeChange


class AutoEditor:
    def __init__(self, dpct_version_root, cta_version_root):
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

        for rule in RULES_TO_DESCRIPTIONS.values():
            rule().run()
            changes = rule.get_tracked_changes()
            for change in changes:
                all_documented_changes.append(change)

        return all_documented_changes
