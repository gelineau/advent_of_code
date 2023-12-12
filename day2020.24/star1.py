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


def get_coordinates(line):
    x = 0
    y = 0
    north_or_south = False
    for char in line:
        if char == "n":
            north_or_south = True
            y -= 1
        elif char == "s":
            north_or_south = True
            y += 1
        elif char == "w":
            if north_or_south:
                x -= 0.5
            else:
                x -= 1
            north_or_south = False
        elif char == "e":
            if north_or_south:
                x += 0.5
            else:
                x += 1
            north_or_south = False
    return (x, y)


def star(filename: str):
    input = list(read_input(filename))
    flipped = Counter(get_coordinates(line) for line in input)
    black_number = len(
        [1 for flipped_number in flipped.values() if flipped_number % 2 == 1]
    )
    return black_number
