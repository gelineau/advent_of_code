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
    "O": [],
    "I": [],
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


def simplify_input(input, cells):
    for row, line in enumerate(input):
        new_line = ""
        for column, cell in enumerate(line):
            if (row, column) in cells:
                new_line += cell
            else:
                new_line += "."
        yield new_line


def display_input(input):
    print()
    for line in input:
        print(line)
    print()


def extend_input_columns(input):
    for row, line in enumerate(input):
        new_line = ""
        for column, cell in enumerate(line):
            new_line += cell
            if east in pipe_directions[cell]:
                new_line += "-"
            else:
                new_line += "."
        yield new_line


def extend_input_lines(input):
    for row, line in enumerate(input):
        yield line
        new_line = ""
        for column, cell in enumerate(line):
            if south in pipe_directions[cell]:
                new_line += "|"
            else:
                new_line += "."
        yield new_line


def is_dot(input, neihbour):
    row, column = neihbour
    if row < 0 or column < 0:
        return False
    try:
        return input[row][column] == "."
    except:
        return False


def replace(input, row, column, value):
    input[row] = input[row][:column] + value + input[row][column + 1 :]


def replace_input(input):
    input[0] = "O" + input[0][1:]

    replaced = True
    while replaced == True:
        replaced = False
        for row, line in enumerate(input):
            for column, cell in enumerate(line):
                if cell == "O":
                    neihbours = get_neighbours((row, column))
                    for neihbour in neihbours:
                        if is_dot(input, neihbour):
                            replace(input, *neihbour, "O")
                            # print(f"replace {neihbour}")
                            replaced = True
    return input


def count(input):
    result = 0
    for row, line in enumerate(input[::2]):
        for column, cell in enumerate(line[::2]):
            if cell == ".":
                result += 1
    return result


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

    simplified_input = list(simplify_input(input, cells))

    for cell, (delta1, delta2) in pipe_directions.items():
        if {add(start, delta1), add(start, delta2)} == {
            start_neighbour1,
            start_neighbour2,
        }:
            print(f"replacing start with {cell}")
            simplified_input[start[0]] = (
                simplified_input[start[0]][: start[1]]
                + cell
                + simplified_input[start[0]][start[1] + 1 :]
            )
            break

    extended_input1 = list(extend_input_columns(simplified_input))
    extended_input2 = list(extend_input_lines(extended_input1))

    replaced_input = replace_input(extended_input2)
    display_input(replaced_input)

    return count(replaced_input)
