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
    def __init__(self, row_intervals, col_intervals):
        self.values = {(0, 0): "."}
        self.max_row_digged = 0
        self.min_row_digged = 0
        self.min_col_digged = 0
        self.max_col_digged = 0
        self.row_intervals = row_intervals
        self.col_intervals = col_intervals

    def get(self, row: int, col: int) -> int:
        return self.values.get((row, col), ".")

    def set(self, row: int, col: int, color: str) -> int:
        self.values[(row, col)] = color
        self.min_row_digged = min(self.min_row_digged, row)
        self.min_col_digged = min(self.min_col_digged, col)
        self.max_row_digged = max(self.max_row_digged, row)
        self.max_col_digged = max(self.max_col_digged, col)

    def __repr__(self):
        result = "\n"
        for row in range(self.min_row_digged, self.max_row_digged + 1):
            result += (
                "".join(
                    self.get(row, column)
                    for column in range(self.min_col_digged, self.max_col_digged + 1)
                )
                + "\n"
            )

        return result

    def fill(self):
        min_row_digged = self.min_row_digged
        max_row_digged = self.max_row_digged
        min_col_digged = self.min_col_digged
        max_col_digged = self.max_col_digged

        for row in range(min_row_digged, max_row_digged + 1):
            print(f"filling {row} sur {max_row_digged}")
            inside = False
            wall = False
            wall_type = None
            for col in range(min_col_digged - 1, max_col_digged + 2):
                if wall and self.get(row, col) != ".":
                    if (
                        self.get(row, col) in ("U", "D")
                        and self.get(row, col) != wall_type
                    ):
                        inside = not inside

                    continue

                if self.get(row, col) == "." and not inside:
                    wall = False
                    self.set(row, col, "O")

                elif self.get(row, col) in ("U", "D"):
                    inside = not inside
                    wall = True
                    wall_type = self.get(row, col)
                else:
                    wall = False

    def neighbours(self, row, col):
        for direction in "UDLR":
            drow, dcol = delta(direction)
            yield row + drow, col + dcol

    def count(self):
        result = 0
        for row in range(self.min_row_digged, self.max_row_digged + 1):
            for col in range(self.min_col_digged, self.max_col_digged + 1):
                if self.get(row, col) != "O":
                    start1, end1 = self.row_intervals[row]
                    start2, end2 = self.col_intervals[col]
                    result += (end1 - start1) * (end2 - start2)
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


def decode(input):
    for line in input:
        color = line["color"]
        line["direction"] = "RDLU"[int(color[-1])]
        line["size"] = int(f"0x{line['color'][:-1]}", base=16)
        yield line


def get_interval_ids(intervals, start, end):
    result = []
    start, end = sorted([start, end])
    for i, interval in enumerate(intervals):
        if start <= interval[0] <= end:
            result.append(i)
    return result


def star(filename: str):
    input = list(read_input(filename))

    input = list(decode(input))
    print(input)

    row_limits = {-1, 0, 1}
    col_limits = {-1, 0, 1}
    row, col = (0, 0)
    for i, line in enumerate(input):
        print(f"{i} sur {len(input)}")
        drow, dcol = delta(line["direction"])

        if line["direction"] in ("U", "D"):
            col_limits.add(col)
            col_limits.add(col + 1)
            row_limits.add(row)
            row_limits.add(row + line["size"] * drow)

            for number in range(0, line["size"] + 1):
                if number != 0:
                    row = row + drow
                    col = col + dcol
        else:
            row_limits.add(row)
            row_limits.add(row + 1)
            col_limits.add(col)
            col_limits.add(col + line["size"] * dcol)

            for number in range(1, line["size"] + 1):
                row = row + drow
                col = col + dcol

    row_limits = sorted(row_limits)
    row_limits.append(row_limits[-1] + 1)
    col_limits = sorted(col_limits)
    col_limits.append(col_limits[-1] + 1)

    row_intervals = [
        (limit1, limit2) for limit1, limit2 in zip(row_limits, row_limits[1:])
    ]
    col_intervals = [
        (limit1, limit2) for limit1, limit2 in zip(col_limits, col_limits[1:])
    ]

    pprint(row_limits)
    pprint(col_limits)

    grid = Grid(row_intervals, col_intervals)
    print("****")
    print(grid)
    print("=====")

    ####### Fill grid with intervals
    row, col = (0, 0)
    for i, line in enumerate(input):
        print(row, col)
        print(f"{i} sur {len(input)}")
        # print(row, col)
        drow, dcol = delta(line["direction"])
        new_row = row + line["size"] * drow
        new_col = col + line["size"] * dcol

        if line["direction"] in ("U", "D"):
            col_interval_id = col_intervals.index((col, col + 1))
            row_interval_ids = get_interval_ids(row_intervals, row, new_row)
            for row_interval_id in row_interval_ids:
                grid.set(row_interval_id, col_interval_id, line["direction"])
        else:
            row_interval_id = row_intervals.index((row, row + 1))
            if line["direction"] == "R":
                col_interval_ids = get_interval_ids(col_intervals, col, new_col)[1:]
            else:
                col_interval_ids = get_interval_ids(col_intervals, col, new_col)[:-1]

            for col_interval_id in col_interval_ids:
                grid.set(row_interval_id, col_interval_id, line["direction"])

        row, col = new_row, new_col

    print(grid)

    grid.fill()

    print(grid)

    return grid.count()
