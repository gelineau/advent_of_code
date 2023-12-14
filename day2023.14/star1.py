from collections import Counter
from dataclasses import dataclass
from functools import lru_cache, cache
from itertools import repeat
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile

from utils import read_dicts_from_input, read_lines_from_input, read_words_from_input


def read_input(filename: str):
    for line in read_lines_from_input(filename):
        yield line


def find_first_non_empty(line: list[str]) -> int:
    for i in range(len(line) - 1, -1, -1):
        if line[i] != ".":
            return i
    return -1


@cache
def tilt_line(line: tuple[str]) -> tuple[str]:
    if line == ():
        return line
    if line[-1] == "#" or line[-1] == "O":
        return tilt_line(line[:-1]) + (line[-1],)
    first_non_empty = find_first_non_empty(line)
    if first_non_empty == -1:
        return line
    if line[first_non_empty] == "#":
        return tilt_line(line[:first_non_empty]) + line[first_non_empty:]

    # it's a O
    return tilt_line(line[:first_non_empty] + line[first_non_empty + 1 :]) + ("O",)


def get_weight(tilted_line):
    total_weight = 0
    for factor, cell in enumerate(tilted_line, start=1):
        if cell == "O":
            total_weight += factor
    return total_weight


def star(filename: str):
    input = list(read_input(filename))

    weight = 0
    for column in range(len(input[0])):
        line = []
        for row in range(len(input) - 1, -1, -1):
            line.append(input[row][column])
        tilted_line = tilt_line(tuple(line))
        weight += get_weight(tilted_line)
        # break  # TODO remove

    return weight
