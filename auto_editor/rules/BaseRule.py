from abc import abstractmethod

from enums import AppliedChange


class BaseRule:
    def __init__(self):
        self.is_run_complete = False

    def run(self):
        self.run_rule()
        self.is_run_complete = True

    @abstractmethod
    def run_rule(self):
        pass

    def get_documented_changes(self):
        if not self.is_run_complete:
            raise Exception("Documented change can only be shown after rule was applied!")

        return self.get_change_items()

    @abstractmethod
    def get_change_items(self) -> AppliedChange:
        # if no change was made, enter "False" for field "was_change_made"
        pass
