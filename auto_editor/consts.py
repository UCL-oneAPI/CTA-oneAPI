DPCT_EXTENSIONS = ('*.dp.cpp', '*.dp.hpp')

# ----- 1049 Constants ------
LOOP_BEGINNING_STR = "parallel_for("

ND_RANGE_PATTERN = "sycl::nd_range<\d+>"

RANGE_OPENER = "sycl::range<{}>({}"
RANGE_ITEM = "{}.get({})"

PARENTHESIS_OPENER = "("
PARENTHESIS_CLOSER = ")"

INDENTATION = "    "
LINE_BREAK = "\n"

GLOBAL_RANGE_IDENTIFIER = "dpct_global_range"
GLOBAL_RANGE_DECLARATION = "auto {} = {} * {};"

MASK_TEMPLATE = "mask_{}"

OPENERS_TO_CLOSERS = {"(": ")",
                      "[": "]",
                      "{": "}"
                      }
# -------
