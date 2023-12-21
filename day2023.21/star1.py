from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile

from utils import read_dicts_from_input, read_lines_from_input, read_words_from_input


from typing import Iterable


class Grid:
    def __init__(self, input: Iterable[str]):
        self.values = [[char for char in line] for line in input]

        for row in range(self.row_max()):
            for col in range(self.col_max()):
                if self.get(row, col) == "S":
                    self.start = (row, col)

    def row_max(self):
        return len(self.values)

    def col_max(self):
        return len(self.values[0])

    def is_in_grid(self, row, column):
        if row < 0 or column < 0 or row >= self.row_max() or column >= self.col_max():
            return False
        return True

    def get(self, row: int, column: int) -> int:
        if self.is_in_grid(row, column):
            return self.values[row][column]
        raise IndexError

    def __repr__(self):
        result = "\n"
        for row in range(self.row_max()):
            result += (
                "".join(str(self.get(row, column)) for column in range(self.col_max()))
                + "\n"
            )

        return result

    def print_positions(self, positions):
        print("\n")
        for row in range(self.row_max()):
            print(
                "".join(
                    str(self.get(row, column))
                    if (row, column) not in positions
                    else "O"
                    for column in range(self.col_max())
                )
            )

    def neighbours(self, row, col):
        for direction in "UDLR":
            drow, dcol = delta(direction)
            if self.is_in_grid(row + drow, col + dcol):
                yield row + drow, col + dcol

    def find_empty_neighbours(self, position):
        for neighbour in self.neighbours(*position):
            if self.get(*neighbour) in [".", "S"]:
                yield neighbour


def delta(move):
    if move == "L":
        return 0, -1
    if move == "R":
        return 0, 1
    if move == "D":
        return 1, 0
    if move == "U":
        return -1, 0
    raise ValueError


def read_input(filename: str):
    grid = Grid(read_lines_from_input(filename))
    print(grid)
    return grid


def move_one_step(grid, positions):
    new_positions = set()

    for position in positions:
        new_positions.update(grid.find_empty_neighbours(position))
    return new_positions


def star(filename: str):
    grid = read_input(filename)

    positions = {grid.start}

    for step in range(64):
        positions = move_one_step(grid, positions)
        grid.print_positions(positions)

    return len(positions)
