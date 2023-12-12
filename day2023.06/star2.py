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


def star(filename: str):
    input = list(read_input(filename))
    times_string, distances_string = input
    time = int("".join((time_string) for time_string in times_string.split()[1:]))
    distance = int(
        "".join((distance_string) for distance_string in distances_string.split()[1:])
    )

    number_of_ways = 0
    for push_time in range(time + 1):
        speed = push_time
        reached_distance = speed * (time - push_time)
        if reached_distance > distance:
            number_of_ways += 1

    return number_of_ways
