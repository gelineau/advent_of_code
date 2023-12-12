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


def get_digits(line: str):
    for char in line:
        if char.isdigit():
            yield char


def star(filename: str):
    lines = list(read_input(filename))
    sum = 0
    for line in lines:
        digits = list(get_digits(line))
        number = int(digits[0] + digits[-1])
        sum += number
    return sum
