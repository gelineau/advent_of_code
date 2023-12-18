from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile

from utils import read_dicts_from_input, read_lines_from_input, read_words_from_input


class Grid:
    def __init__(self):
        self.size = 1000
        self.values = [["." for _ in range(self.size)] for _ in range(self.size)]
        self.min_row_digged = self.size // 2
        self.max_row_digged = self.size // 2
        self.min_col_digged = self.size // 2
        self.max_col_digged = self.size // 2

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

    def set(self, row: int, col: int, color: str) -> int:
        if not self.is_in_grid(row, col):
            raise IndexError
        self.values[row][col] = color
        self.min_row_digged = min(self.min_row_digged, row)
        self.min_col_digged = min(self.min_col_digged, col)
        self.max_row_digged = max(self.max_row_digged, row)
        self.max_col_digged = max(self.max_col_digged, col)

    def __repr__(self):
        result = "\n"
        for row in range(self.min_row_digged, self.max_row_digged + 1):
            result += (
                "".join(
                    (
                        "C"
                        if self.get(row, column) not in (".", "O")
                        else self.get(row, column)
                    )
                    for column in range(self.min_col_digged, self.max_col_digged + 1)
                )
                + "\n"
            )

        return result

    def fill(self):
        self.set(self.min_row_digged, self.min_col_digged - 1, "O")

        min_row_digged = self.min_row_digged
        max_row_digged = self.max_row_digged
        min_col_digged = self.min_col_digged
        max_col_digged = self.max_col_digged

        changed = True
        while changed:
            changed = False
            for row in range(min_row_digged - 1, max_row_digged + 2):
                for col in range(min_col_digged - 1, max_col_digged + 2):
                    if self.get(row, col) != ".":
                        continue
                    if any(
                        self.get(*neighbour) == "O"
                        for neighbour in self.neighbours(row, col)
                    ):
                        self.set(row, col, "O")
                        changed = True

    def neighbours(self, row, col):
        for direction in "UDLR":
            drow, dcol = delta(direction)
            yield row + drow, col + dcol

    def count(self):
        result = 0
        for row in range(self.min_row_digged, self.max_row_digged + 1):
            for col in range(self.min_col_digged, self.max_col_digged + 1):
                if self.get(row, col) != "O":
                    result += 1
        return result


def read_input(filename: str):
    template = "{direction} {size:d} (#{color})"
    for values in read_dicts_from_input(filename, template):
        yield values


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


def star(filename: str):
    input = list(read_input(filename))
    print(input)
    grid = Grid()
    print("****")
    print(grid)
    print("=====")

    row, col = (grid.size // 2, grid.size // 2)
    for line in input:
        drow, dcol = delta(line["direction"])
        for number in range(1, line["size"] + 1):
            row = row + drow
            col = col + dcol
            # print(f"{row=} {col=}")
            grid.set(row, col, line["color"])

    print(grid)

    grid.fill()

    print(grid)

    return grid.count()
