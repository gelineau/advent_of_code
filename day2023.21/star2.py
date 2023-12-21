import sys
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache, cache
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

    # def find_empty_neighbours(self, position):
    #     for neighbour in self.neighbours(*position):
    #         if self.get(*neighbour) in [".", "S"]:
    #             yield neighbour

    def find_empty_neighbours(self, position):
        for direction in "UDLR":
            new_position = list(add(delta(direction), position))

            if new_position[0] < 0:
                row_grid = -1
                new_position[0] += self.row_max()
            elif new_position[0] >= self.row_max():
                row_grid = +1
                new_position[0] -= self.row_max()
            else:
                row_grid = 0

            if new_position[1] < 0:
                col_grid = -1
                new_position[1] += self.col_max()
            elif new_position[1] >= self.col_max():
                col_grid = +1
                new_position[1] -= self.col_max()
            else:
                col_grid = 0

            if self.get(*new_position) in [".", "S"]:
                yield (row_grid, col_grid), tuple(new_position)


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


def add(grid_position, new_grid_position):
    return (
        grid_position[0] + new_grid_position[0],
        grid_position[1] + new_grid_position[1],
    )


@cache
def move_steps(position, n):
    if n == 0:
        return {((0, 0), position)}

    all_positions = set()

    for bunch in [
        1000_000,
        100_000,
        1000,
        250,
        200,
        180,
        150,
        120,
        100,
        70,
        50,
        25,
        20,
        10,
        4,
        2,
    ]:
        if n > bunch:
            for grid_position, inside_position in move_steps(position, bunch):
                new_positions = move_steps(inside_position, n - bunch)
                for new_grid_position, new_inside_position in new_positions:
                    all_positions.add(
                        (add(grid_position, new_grid_position), new_inside_position)
                    )
            return all_positions

    for grid_position, inside_position in move_steps(position, n - 1):
        new_positions = find_neighbours(inside_position)
        for new_grid_position, new_inside_position in new_positions:
            all_positions.add(
                (add(grid_position, new_grid_position), new_inside_position)
            )
    return all_positions


@cache
def find_neighbours(position):
    return tuple(grid.find_empty_neighbours(position))


# def move_one_step(grid, positions):
#     all_positions = set()
#
#     for grid_position, inside_position in positions:
#         new_positions = grid.find_empty_neighbours(inside_position)
#         for new_grid_position, new_inside_position in new_positions:
#             all_positions.add(
#                 (add(grid_position, new_grid_position), new_inside_position)
#             )
#     return all_positions


grid = None


def star(filename: str):
    global grid

    grid = read_input(filename)

    position = grid.start

    sys.setrecursionlimit(1000)

    for step in range(1, 500):
        positions = move_steps(position, step)
        print(
            step,
            len(
                [1 for grid_position, position in positions if grid_position == (0, 0)]
            ),
            len({grid_position for grid_position, position in positions}),
        )

    return len(positions)
