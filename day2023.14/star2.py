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
        yield tuple(line)


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


def calculate_north_weight(input):
    weight = 0
    for column in range(len(input[0])):
        line = []
        for row in range(len(input) - 1, -1, -1):
            line.append(input[row][column])
        weight += get_weight(line)
    return weight


@cache
def move_north(input):
    columns = []
    for col in range(len(input[0])):
        column = []
        for row in range(len(input) - 1, -1, -1):
            column.append(input[row][col])
        tilted_column = tilt_line(tuple(column))
        columns.append(tuple(reversed(tilted_column)))

    lines = []

    for row in range(len(input)):
        lines.append(tuple(column[row] for column in columns))

    return tuple(lines)


@cache
def move_south(input):
    columns = []
    for col in range(len(input[0])):
        column = []
        for row in range(len(input)):
            column.append(input[row][col])
        tilted_column = tilt_line(tuple(column))
        columns.append(tilted_column)

    lines = []

    for row in range(len(input)):
        lines.append(tuple(column[row] for column in columns))

    return tuple(lines)


@cache
def move_west(input):
    rows = []
    for row, line in enumerate(input):
        tilted_line = tilt_line(tuple(reversed(line)))
        rows.append(tuple(reversed(tilted_line)))
    return tuple(rows)


@cache
def move_east(input):
    rows = []
    for row, line in enumerate(input):
        tilted_line = tilt_line(line)
        rows.append(tuple(tilted_line))
    return tuple(rows)


@cache
def move_cycle(input):
    input = move_north(input)
    input = move_west(input)
    input = move_south(input)
    input = move_east(input)
    return input


def star(filename: str):
    input = tuple(read_input(filename))
    # weights = {}
    # # for step in range(3):
    # for step in range(1_000_000_000):
    #     # if step % 1_000_000 == 0:
    #     #     print(step / 1_000_000)
    #     input = move_cycle(input)
    #     weight = calculate_north_weight(input)
    #     if weight in weights:
    #         print(
    #             f"{step=} {weight=} already seen on step {weights[weight]} difference {step-weights[weight]}"
    #         )
    #
    #     weights[weight] = step

    cycle = 42
    for step in range(1_000_000_000 - cycle * 23809000):
        input = move_cycle(input)

    return calculate_north_weight(input)
