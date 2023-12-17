from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile

from utils import read_dicts_from_input, read_lines_from_input, read_words_from_input


def add(position, direction):
    return position[0] + direction[0], position[1] + direction[1]


up = -1, 0
down = 1, 0
left = 0, -1
right = 0, 1


def is_in(position, input):
    row, column = position
    if row < 0:
        return False
    if column < 0:
        return False
    if row >= len(input):
        return False
    if column >= len(input[0]):
        return False
    return True


def go_through(position, direction, input):
    drow, dcolumn = direction
    mirror = input[position[0]][position[1]]
    if mirror == "/":
        new_directions = [(-dcolumn, -drow)]
    elif mirror == "\\":
        new_directions = [(dcolumn, drow)]
    elif mirror == ".":
        new_directions = [direction]
    elif mirror == "|" and dcolumn == 0:
        new_directions = [direction]
    elif mirror == "-" and drow == 0:
        new_directions = [direction]
    elif mirror == "|":
        new_directions = [up, down]
    elif mirror == "-":
        new_directions = [left, right]
    else:
        raise ValueError

    new_states = [
        (add(position, new_direction), new_direction)
        for new_direction in new_directions
    ]
    return [
        (position, direction)
        for position, direction in new_states
        if is_in(position, input)
    ]


def read_input(filename: str):
    for line in read_lines_from_input(filename):
        yield line


def calculate_length(input, states):
    seen_states = set(states)
    while states:
        state = states.pop()
        new_states = go_through(*state, input)
        for new_state in new_states:
            if new_state not in seen_states:
                states.append(new_state)
        seen_states = seen_states.union(new_states)
    seen_positions = sorted(set(position for (position, direction) in seen_states))
    return len(seen_positions)


def star(filename: str):
    input = list(read_input(filename))

    states = [((0, 0), right)]
    return calculate_length(input, states)
