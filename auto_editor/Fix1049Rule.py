import logging
import re
from typing import List, Tuple, Dict

from auto_editor.BaseRule import BaseRule
from auto_editor.LineItem import LineItem
from auto_editor.StructuredProjectSource import StructuredProjectSource
from enums import ChangeTypeEnum


class Fix1049Rule(BaseRule):
    @property
    def dpct_warning_codes(self) -> List[str]:
        return ["DPCT1049"]

    @property
    def change_type(self) -> ChangeTypeEnum:
        return ChangeTypeEnum.fix

    def run_rule(self, project: StructuredProjectSource,
                 warning_first_line: int, warning_last_line: int, file_path: str) -> StructuredProjectSource:
        loop_beginning_str = "parallel_for("
        file_lines = project.paths_to_lines[file_path]
        for i in range(warning_last_line + 1, len(file_lines)):
            current_line = file_lines[i]
            is_loop_starts = loop_beginning_str in current_line.code
            if is_loop_starts:
                vec_len, (vec_1, vec_2) = self.get_range_len(i, file_lines)
                self.add_vec_product_declaration(vec_1, vec_2)
                self.delete_dpct_warning()
                self.reverse_ranges()
        return project

    def get_range_len(self, loop_beginning: int, file_lines: List[LineItem]) -> (int, Tuple[str, str]):
        nd_range_pattern = 'sycl::nd_range<\d+>'
        for i in range(loop_beginning, loop_beginning + 2):
            # nd_range must be at same or next line as loop beginning
            code = file_lines[i].code
            result = re.search(nd_range_pattern, code)
            if result:
                vec_names = self.get_vector_names(result, i, file_lines)
                range_len = int(result.group()[result.group().index('<') + 1:-1])
                return (range_len, vec_names)

        logging.exception("Fix of DPCT1049: no nd_range declared in loop.")

    def get_vector_names(self, regex_result, opening_line_i, file_lines: List[LineItem]):
        opener_i = regex_result.regs[0][1]
        (closing_line_i, closer_i) = self.get_closing_of_parentheses(opening_line_i, opener_i, file_lines)
        joined_code = self.join_code(opening_line_i, opener_i + 1, closing_line_i, closer_i, file_lines)
        masked_code, masks_to_values = self.mask_code_params(joined_code)
        params_with_multiply = re.findall("(?:,|\*|[^\s,^\*,^,]*)", masked_code)
        params_with_multiply = [e for e in params_with_multiply if not e == '']
        if not params_with_multiply[1] == '*' and params_with_multiply[3] == ',':
            raise Exception('Fix 1049: Code structure different than expected. Cannot resolve.')

        vec_1 = self.unmask(params_with_multiply[0], masks_to_values)
        vec_2 = self.unmask(params_with_multiply[2], masks_to_values)

        return vec_1, vec_2

    def unmask(self, code: str, masks_to_values: Dict[str, str]):
        for mask, val in masks_to_values.items():
            if mask in code:
                return code.replace(mask, val)

        raise Exception("Mask does not exist")

    def mask_code_params(self, str) -> (str, dict):
        masks_to_values = {}
        masked_full_code = ''
        enclosing_locations = self.get_all_enclosings_locations(str)
        start_i = 0
        for loc_tuple in enclosing_locations:
            masked_params = str[loc_tuple[0] + 1: loc_tuple[1]]
            if masked_params in masks_to_values.values():
                mask_name = list(masks_to_values.keys())[list(masks_to_values.values()).index(masked_params)]
            else:
                mask_name = "mask_" + f'{start_i}'
                masks_to_values[mask_name] = masked_params

            closer = str[loc_tuple[1]]
            masked_full_code += str[start_i:loc_tuple[0] + 1]
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

    def get_closing_of_parentheses(self, line_index: int, opener_index, file_lines: List[LineItem]) -> (int, int):
        openers_to_closers = {'(': ')',
                              '[': ']',
                              '{': '}'
                              }
        opener = file_lines[line_index].code[opener_index]
        closer = openers_to_closers[opener]

        inner_openers = 0
        inner_closers = 0
        is_first_line = True
        for line in range(line_index, len(file_lines)):
            line_code = file_lines[line].code
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

    def join_code(self, first_line: int, first_char: int, last_line: int, last_char: int, file_lines) -> str:
        all_code = ''
        for i in range(first_line, last_line + 1):
            line_code = file_lines[i].code
            if i == first_line:
                line_code = line_code[first_char:]
            if i == last_line:
                line_code = line_code[:last_char + 1]

            clean_line = line_code.strip()  # remove excessive spaces
            if clean_line[:-2] == '\n':
                clean_line = clean_line[:-2] + ' '  # replace "\n" with single space

            all_code += clean_line

        return all_code
