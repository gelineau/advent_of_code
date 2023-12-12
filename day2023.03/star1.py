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

def get_value(input: list[str], row: int, col: int)-> str:
    if row < 0 or col <0:
        return "."

    try:
        return input[row][col]
    except IndexError:
        return "."


def get_number_positions_from_line(input, max_cols, row):
    first_digit_col = None
    for col in range(max_cols+1):
        is_current_digit = get_value(input, row, col).isdigit()
        match (first_digit_col, is_current_digit):
            case (None, True):
                first_digit_col = col
            case (None, False):
                pass
            case (_, True):
                pass
            case (_, False):
                yield (row, first_digit_col, col)
                first_digit_col = None



def get_number_positions(input, max_rows, max_cols):
    for row, line in enumerate(input):
        yield from get_number_positions_from_line(input, max_cols, row)


def get_neighbour_positions(row, min_col, max_col):
    for col in range(min_col-1, max_col+1):
        yield (row-1, col)
        yield (row+1, col)
    yield (row, min_col-1)
    yield (row, max_col)



def has_symbol_neighbour(input, row, min_col, max_col):
    if row==4:
        pass
    neighbour_positions = list(get_neighbour_positions(row, min_col, max_col))
    values = [get_value(input, row, col) for row, col in neighbour_positions]
    return any(value != "." and not value.isdigit() for value in values)

def star(filename: str):
    input = list(read_input(filename))
    max_rows = len(input)
    max_cols = len(input[0])

    print(f"{max_rows=} {max_cols=}")

    number_positions = list(get_number_positions(input, max_rows, max_cols))
    pprint(number_positions)

    sum_value = 0
    for row, min_col, max_col in number_positions:
        if  has_symbol_neighbour(input, row, min_col, max_col):
            sum_value += int(input[row][min_col:max_col])

    return sum_value


