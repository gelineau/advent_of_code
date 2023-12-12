from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat, combinations
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile

from utils import read_dicts_from_input, read_lines_from_input, read_words_from_input

#
# def expand_rows(input, row_galaxies):
#     for row, line in enumerate(input):
#         yield line
#         if row not in row_galaxies:
#             yield line


def read_input(filename: str):
    input = list(read_lines_from_input(filename))

    row_galaxies = set()
    columns_galaxies = set()
    galaxies = set()

    for row, line in enumerate(input):
        for column, cell in enumerate(line):
            if cell == "#":
                row_galaxies.add(row)
                columns_galaxies.add(column)
                galaxies.add((row, column))

    # input = list(expand_rows(input, row_galaxies))
    return galaxies, row_galaxies, columns_galaxies


def shortest_path(galaxy1, galaxy2, empty_rows, empty_columns):
    row1 = min(galaxy1[0], galaxy2[0])
    row2 = max(galaxy1[0], galaxy2[0])
    column1 = min(galaxy1[1], galaxy2[1])
    column2 = max(galaxy1[1], galaxy2[1])

    delta = row2 - row1 + sum(1 for row in empty_rows if row1 < row < row2)
    delta += (
        column2
        - column1
        + sum(1 for column in empty_columns if column1 < column < column2)
    )

    return delta


def star(filename: str):
    galaxies, row_galaxies, columns_galaxies = list(read_input(filename))

    empty_rows = set(range(max(row_galaxies))) - row_galaxies
    empty_columns = set(range(max(columns_galaxies))) - columns_galaxies
    return sum(
        shortest_path(galaxy1, galaxy2, empty_rows, empty_columns)
        for galaxy1, galaxy2 in combinations(galaxies, 2)
    )
