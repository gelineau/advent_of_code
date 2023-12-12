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


north = (-1, 0)
south = (+1, 0)
east = (0, +1)
west = (0, -1)

pipe_directions = {
    "|": [north, south],
    "-": [east, west],
    "L": [north, east],
    "J": [north, west],
    "7": [south, west],
    "F": [south, east],
    ".": [],
    "S": [],
}


def get_neighbours(cell: tuple[int, int]) -> Iterator[tuple[int, int]]:
    for delta in (north, south, east, west):
        yield add(cell, delta)


def add(cell: tuple[int, int], delta: tuple[int, int]) -> tuple[int, int]:
    return cell[0] + delta[0], cell[1] + delta[1]


def get_cell(input: list[str], row: int, column: int) -> str:
    if row < 0 or column < 0:
        return "."
    try:
        return input[row][column]
    except IndexError:
        return "."


def get_connected(input: list[str], row: int, column: int) -> list[tuple[int, int]]:
    cell = get_cell(input, row, column)
    return pipe_directions[cell]


def get_start(input: list[str]) -> tuple[int, int]:
    for row, line in enumerate(input):
        for column in range(len(line)):
            if get_cell(input, row, column) == "S":
                return row, column
    raise ValueError


def is_connected(
    input: list[str], neighbour: tuple[int, int], start: tuple[int, int]
) -> bool:
    deltas = get_connected(input, *neighbour)
    if not deltas:
        return False
    delta1, delta2 = deltas
    if add(delta1, neighbour) == start:
        return True
    if add(delta2, neighbour) == start:
        return True
    return False


def get_next(
    input: list[str], before: tuple[int, int], cell: tuple[int, int]
) -> tuple[int, int]:
    deltas = get_connected(input, *cell)
    if not deltas:
        raise ValueError
    delta1, delta2 = deltas
    if add(delta1, cell) == before:
        return add(delta2, cell)
    return add(delta1, cell)


def star(filename: str):
    input = list(read_input(filename))
    start = get_start(input)

    start_neighbour1, start_neighbour2 = [
        neighbour
        for neighbour in get_neighbours(start)
        if is_connected(input, neighbour, start)
    ]

    cells = [start, start_neighbour1]

    while True:
        cells.append(get_next(input, *cells[-2:]))
        if cells[-1] == start_neighbour2:
            break

    return len(cells) // 2
