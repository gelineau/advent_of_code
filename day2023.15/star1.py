from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile

from utils import (
    read_dicts_from_input,
    read_lines_from_input,
    read_words_from_input,
    read_text_from_input,
)


def read_input(filename: str):
    line = read_text_from_input(filename)

    return line.split(",")


def calculate_hash(word):
    result = 0
    for char in word:
        result += ord(char)
        result *= 17
        result = result % 256
    return result


def star(filename: str):
    print(calculate_hash("HASH"))
    input = list(read_input(filename))
    return sum(calculate_hash(word) for word in input)
