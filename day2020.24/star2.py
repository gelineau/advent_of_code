from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile

from utils import read_dicts_from_input, read_lines_from_input, read_words_from_input


def read_input(filename: str):
    for line in read_lines_from_input(filename):
        yield line

    # for words in read_words_from_input(filename):
    #     yield words
    #
    # template = "{min1:d}-{max1:d},{min2:d}-{max2:d}"
    # for values in read_dicts_from_input(filename, template):
    #     yield values


def star(filename: str):
    input = list(read_input(filename))
    return 42
