import re
from uuid import uuid4


class LineItem:
    def __init__(self, code: str, original_line: int = None):
        self.id = uuid4()  # unique ID for each line
        self.code = code
        self.original_line = original_line  # lines always start counting from zero

    def get_dpct_warning_code(self):
        pattern = ".*(DPCT\d{4}):\d+: "
        code_line = self.code.lstrip()
        result = re.search(pattern, code_line)

        warning_code = None
        if result:
            warning_code = result.group(1)
        return warning_code