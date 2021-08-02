from typing import List

from constants import RULES_TO_DESCRIPTIONS
from enums import AppliedChange


class AutoEditor:
    def __init__(self, dpct_version_root, cta_version_root):
        self.dpct_version_root = dpct_version_root
        self.cta_version_root = cta_version_root

    def make_changes(self) -> List[AppliedChange]:
        '''
        apply the different rules to create the new version in self.cta_version_root.
        changes are documented as they are made and returned in documented_changes

        :return:
        documented_changes: list of changes. Format: namedTuple AppliedChange
        '''

        all_documented_changes = []

        for rule in RULES_TO_DESCRIPTIONS.values():
            rule.run()
            changes = rule.get_documented_changes()
            for change in changes:
                all_documented_changes.append(change)

        return self.clean_changes(all_documented_changes)

    def clean_changes(self, changes: List[AppliedChange]) -> List[AppliedChange]:
        '''
        removes all empty changes items, i.e. where was_change_made=False
        '''
        return []
