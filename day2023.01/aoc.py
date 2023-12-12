from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile

import star1
import star2
from utils import read_dicts_from_input, read_lines_from_input, read_words_from_input


filenames_star1 = [
    # "puzzle_simpletest1.txt",
    # "puzzle_test.txt",
    "puzzle.txt",
]

for filename in filenames_star1:
    print(f"{filename=} {star1.star(filename)=}")


filenames_star2 = [
    "puzzle_test.txt",
    "puzzle.txt",
    "puzzle_simpletest1.txt",
]
for filename in filenames_star2:
    print(f"{filename=} {star2.star(filename)=}")


# 55645 is too low
# 55653 is wrong
