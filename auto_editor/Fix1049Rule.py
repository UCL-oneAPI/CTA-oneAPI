import logging
import re
import uuid
from typing import List, Tuple, Dict

from auto_editor.BaseRule import BaseRule
from auto_editor.LineItem import LineItem
from auto_editor.StructuredProjectSource import StructuredProjectSource
from auto_editor.constants import ND_RANGE_PATTERN, RANGE_ITEM, INDENTATION, RANGE_OPENER, RANGE_CLOSER, LINE_BREAK
from auto_editor.utils import get_index_of_line_id
from enums import ChangeTypeEnum

'''
- read through and clean
- merge master into this
- move self.file_lines to base class
- write tests
'''


class Fix1049Rule(BaseRule):
    def __init__(self):
        super().__init__()
        self.new_vec_name = "dpct_global_range"
        self.file_lines = []

    @property
    def dpct_warning_codes(self) -> List[str]:
        return ["DPCT1049"]

    @property
    def change_type(self) -> ChangeTypeEnum:
        return ChangeTypeEnum.fix

    def run_rule(self, project: StructuredProjectSource,
                 warning_first_line: int, warning_last_line: int, file_path: str) -> StructuredProjectSource:
        loop_beginning_str = "parallel_for("
        self.file_lines = project.paths_to_lines[file_path]
        warning_begin_id = self.file_lines[warning_first_line].id
        warning_end_id = self.file_lines[warning_last_line].id
        for i in range(warning_last_line + 1, len(self.file_lines)):
            current_line = self.file_lines[i]
            is_loop_starts = loop_beginning_str in current_line.code
            if is_loop_starts:
                vec_len, range_line_id, (vec_1, vec_2) = self.get_range_details(i)
                self.add_vec_product_declaration(vec_1, vec_2, i)
                self.reverse_ranges(vec_len, vec_2, range_line_id)
                self.delete_dpct_warning(warning_begin_id, warning_end_id)
                project.paths_to_lines[file_path] = self.file_lines
                break
        return project

    def add_vec_product_declaration(self, vec_1, vec_2, loop_begin_i: int):
        indentation = self.get_indentation(self.file_lines[loop_begin_i].code)
        declaration = f"{indentation}auto {self.new_vec_name} = {vec_1} * {vec_2};"
        new_lines = [declaration, '']
        self.add_code(new_lines, loop_begin_i)

    def get_range_details(self, loop_beginning: int) -> (int, uuid, Tuple[str, str]):
        for i in range(loop_beginning, loop_beginning + 2):
            # nd_range must be at same or next line as loop beginning
            code = self.file_lines[i].code
            result = re.search(ND_RANGE_PATTERN, code)
            if result:
                vec_names = self.get_vector_names(result, i)
                range_len = int(result.group()[result.group().index('<') + 1:-1])
                return range_len, self.file_lines[i].id, vec_names

        logging.exception("Fix of DPCT1049: no nd_range declared in loop.")

    def get_vector_names(self, regex_result, opening_line_i):
        opener_i = regex_result.regs[0][1]
        (closing_line_i, closer_i) = self.get_closing_of_parentheses(opening_line_i, opener_i)
        joined_code = self.join_code(opening_line_i, opener_i + 1, closing_line_i, closer_i)

        # sometimes, what is passed as params are not just identifiers, but more complex code syntax.
        # That can break the regex. Hence, the params are first masked with a mock identifier, and later unmasked again
        masked_code, masks_to_values = self.mask_code_params(joined_code)
        params_with_multiply = re.findall("(?:,|\*|[^\s,^\*,^,]*)", masked_code)
        params_with_multiply = [e for e in params_with_multiply if not e == '']
        if not params_with_multiply[1] == '*' and params_with_multiply[3] == ',':
            raise Exception('Fix 1049: Code structure different than expected. Cannot resolve.')

        vec_1 = self.unmask(params_with_multiply[0], masks_to_values) if masks_to_values else params_with_multiply[0]
        vec_2 = self.unmask(params_with_multiply[2], masks_to_values) if masks_to_values else params_with_multiply[2]

        return vec_1, vec_2

    def unmask(self, code: str, masks_to_values: Dict[str, str]):
        for mask, val in masks_to_values.items():
            if mask in code:
                return code.replace(mask, val)

        raise Exception("Mask does not exist")

    def mask_code_params(self, code_str) -> (str, dict):
        masks_to_values = {}
        masked_full_code = ''
        enclosing_locations = self.get_all_enclosings_locations(code_str)
        start_i = 0
        if not enclosing_locations:
            return code_str, {}
        for loc_tuple in enclosing_locations:
            masked_params = code_str[loc_tuple[0] + 1: loc_tuple[1]]
            if masked_params in masks_to_values.values():
                mask_name = list(masks_to_values.keys())[list(masks_to_values.values()).index(masked_params)]
            else:
                mask_name = "mask_" + f'{start_i}'
                masks_to_values[mask_name] = masked_params

            closer = code_str[loc_tuple[1]]
            masked_full_code += code_str[start_i:loc_tuple[0] + 1]
            masked_full_code += mask_name + closer

            start_i = loc_tuple[1] + 1

        return masked_full_code, masks_to_values

    def get_all_enclosings_locations(self, str) -> List[tuple]:
        same_level_enclosings = []
        start_index = 0
        while True:
            location_tuple = self.get_next_matching_enclosing_location(str[start_index:])
            if not location_tuple:
                break
            same_level_enclosings.append((location_tuple[0] + start_index,
                                          location_tuple[1] + start_index))
            start_index += location_tuple[1] + 1
        return same_level_enclosings

    def get_next_matching_enclosing_location(self, str) -> (int, int):
        opener = '('
        closer = ')'
        inner_openers = 0
        inner_closers = 0
        first_opener_i = None
        for i in range(len(str)):
            if str[i] == opener:
                inner_openers += 1
                if inner_openers == 1:
                    first_opener_i = i
            if str[i] == closer:
                inner_closers += 1
                if inner_openers == inner_closers:
                    return (first_opener_i, i)

        if inner_openers == 0:
            return None
        else:
            raise Exception('Corresponding closing character could not be found.')

    def get_closing_of_parentheses(self, line_index: int, opener_index) -> (int, int):
        openers_to_closers = {'(': ')',
                              '[': ']',
                              '{': '}'
                              }
        opener = self.file_lines[line_index].code[opener_index]
        closer = openers_to_closers[opener]

        inner_openers = 0
        inner_closers = 0
        is_first_line = True
        for line in range(line_index, len(self.file_lines)):
            line_code = self.file_lines[line].code
            first_char_i = opener_index if is_first_line else 0
            for char_i in range(first_char_i + 1, len(line_code)):
                if line_code[char_i] == opener:
                    inner_openers += 1
                if line_code[char_i] == closer:
                    if inner_openers != inner_closers:
                        inner_closers += 1
                    else:
                        return (line, char_i)
            is_first_line = False

        raise Exception('Corresponding closing character could not be found.')

    def join_code(self, first_line: int, first_char: int, last_line: int, last_char: int) -> str:
        all_code = ''
        for i in range(first_line, last_line + 1):
            line_code = self.file_lines[i].code
            if i == first_line:
                line_code = line_code[first_char:]
            if i == last_line:
                line_code = line_code[:last_char + 1]

            clean_line = line_code.strip()  # remove excessive spaces
            if clean_line[:-2] == '\n':
                clean_line = clean_line[:-2] + ' '  # replace "\n" with single space

            all_code += clean_line

        return all_code

    def reverse_ranges(self, vec_len: int, vec_2: str, range_line_id: uuid):
        range_begin = get_index_of_line_id(range_line_id, self.file_lines)
        line_of_range = self.file_lines[range_begin]
        result = re.search(ND_RANGE_PATTERN, line_of_range.code)
        opener_i = result.regs[0][1]
        (closing_line_i, closer_i) = self.get_closing_of_parentheses(range_begin, opener_i)
        new_range_first_line = line_of_range.code[:opener_i + 1]
        new_range_end_line = self.file_lines[closing_line_i].code[closer_i:]
        indentation = self.get_indentation(new_range_first_line) + INDENTATION
        new_codes = [new_range_first_line]

        self.remove_code(range_begin, closing_line_i)

        reversed_new_vec = self.reverse_range(self.new_vec_name, vec_len, indentation)
        reversed_new_vec[-1] += ','
        new_codes.extend(reversed_new_vec)

        reversed_vec_2 = self.reverse_range(vec_2, vec_len, indentation)
        reversed_vec_2[-1] += new_range_end_line
        new_codes.extend(reversed_vec_2)

        self.add_code(new_codes, range_begin)

    def reverse_range(self, name, len, indentation) -> List[str]:
        items = []
        biggest_i = len - 1
        for i in range(len):
            current_i = biggest_i - i
            new_item = RANGE_ITEM.format(name, current_i)
            if i == 0:
                code = indentation + RANGE_OPENER.format(len, new_item)
                indentation += INDENTATION
            else:
                code = indentation + new_item

            is_last = current_i == 0
            if not is_last:
                code += ','
            else:
                code += RANGE_CLOSER

            items.append(code)
        return items

    def get_indentation(self, code_line: str):
        indentation = ''
        for char in code_line:
            if char == ' ':
                indentation += char
            else:
                break
        return indentation

    def add_code(self, lines: List[str], index: int):
        # add line break if not exists yet
        lines_with_break = [l + LINE_BREAK if not LINE_BREAK in l else l for l in lines]

        line_items = [LineItem(code) for code in lines_with_break]
        self.file_lines[index: index] = line_items

    def remove_code(self, first_line: int, last_line: int = None):
        remaining_line = last_line + 1 if last_line else first_line + 1
        del self.file_lines[first_line: remaining_line]

    def delete_dpct_warning(self, warning_begin_id, warning_end_id):
        warning_begin_i = get_index_of_line_id(warning_begin_id, self.file_lines)
        warning_end_i = get_index_of_line_id(warning_end_id, self.file_lines)
        self.remove_code(warning_begin_i, warning_end_i)
