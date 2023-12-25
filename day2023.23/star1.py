import sys
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from pprint import pprint
from typing import Iterator, List, Optional, Any, Iterable
from parse import compile

from utils import read_dicts_from_input, read_lines_from_input, read_words_from_input


class Grid:
    def __init__(self, input: Iterable[str]):
        self.values = [[char for char in line] for line in input]
        self.start_col = [
            col for col, value in enumerate(self.values[0]) if value == "."
        ][0]

    def row_max(self):
        return len(self.values)

    def col_max(self):
        return len(self.values[0])

    def is_in_grid(self, row, column):
        if row < 0 or column < 0 or row >= self.row_max() or column >= self.col_max():
            return False
        return True

    def get(self, row: int, column: int) -> str:
        if self.is_in_grid(row, column):
            return self.values[row][column]
        raise IndexError

    def set(self, row: int, col: int, color: str):
        if not self.is_in_grid(row, col):
            raise IndexError
        self.values[row][col] = color

    def get_point_repr(self, row, col, path):
        if (row, col) in path:
            return "O"
        if row == 0 and col == self.start_col:
            return "S"
        return self.get(row, col)

    def display(self, path=()):
        result = "\n"
        for row in range(self.row_max()):
            result += (
                "".join(
                    self.get_point_repr(row, column, path)
                    for column in range(self.col_max())
                )
                + "\n"
            )

        print(result)

    def neighbours(self, row, col):
        for direction in "UDLR":
            drow, dcol = delta(direction)
            if self.is_in_grid(row + drow, col + dcol):
                yield row + drow, col + dcol

    def empty_neighbours(self, row, col):
        for neighbour in self.neighbours(row, col):
            if self.get(*neighbour) == ".":
                yield neighbour
            elif self.get(*neighbour) == "#":
                continue
            elif add((row, col), delta(self.get(*neighbour))) == neighbour:
                yield neighbour

    def get_paths(self, path_so_far, start):
        # print()
        # self.display(path_so_far)
        for neighbour in self.empty_neighbours(*start):
            if neighbour in path_so_far:
                continue
            new_path = deepcopy(path_so_far)
            new_path.add(neighbour)
            if neighbour[0] == self.row_max() - 1:
                yield path_so_far
            else:
                yield from self.get_paths(new_path, neighbour)


def add(point1, point2):
    return (point1[0] + point2[0], point1[1] + point2[1])


def delta(move):
    if move == "L" or move == "<":
        return 0, -1
    if move == "R" or move == ">":
        return 0, 1
    if move == "D" or move == "v":
        return 1, 0
    if move == "U" or move == "^":
        return -1, 0
    raise ValueError(move)


def read_input(filename: str):
    return Grid(read_lines_from_input(filename))


def star(filename: str):
    sys.setrecursionlimit(10000)

    grid = read_input(filename)
    grid.display()
    return max(
        [
            len(path)
            for path in grid.get_paths({(0, grid.start_col)}, (0, grid.start_col))
        ]
    )
