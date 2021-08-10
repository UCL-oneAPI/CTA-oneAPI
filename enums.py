from collections import namedtuple
from enum import Enum


class DiffOperationEnum(Enum):
    add = 'a'
    delete = 'd'


class ChangeTypeEnum(Enum):
    fix = 'fix'
    recommendation = 'recommendation'


WarningItem = namedtuple('WarningItem', 'project_name warning_code file_path message line')

CodeChange = namedtuple('CodeChange', 'edit_id path_to_file line_id diff_operation rule change_type')

WarningLocation = namedtuple('WarningLocation', 'first_line_id last_line_id file_path')
