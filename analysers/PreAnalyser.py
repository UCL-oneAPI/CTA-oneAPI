from typing import List

from analysers.BaseAnalyser import BaseAnalyser
from enums import WarningItem


class PreAnalyser(BaseAnalyser):

    def get_all_warnings(self) -> List[WarningItem]:
        all_warnings = self.get_warnings()
        return all_warnings
