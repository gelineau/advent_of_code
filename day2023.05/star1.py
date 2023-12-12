from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile

from utils import read_dicts_from_input, read_lines_from_input, read_words_from_input


def read_input(filename: str):
    input = open(filename).read()
    paragraphs = input.split("\n\n")
    soils = [int(value) for value in paragraphs[0].split()[1:]]
    yield soils
    for paragraph in paragraphs[1:]:
        values = []
        for line in paragraph.split("\n"):
            print(line)
            if "map" in line:
                continue
            values.append([int(value) for value in line.split()])
        yield values


def transform(value, map):
    for destination_range_start, source_range_start, range_length in map:
        if source_range_start <= value <= source_range_start + range_length:
            return destination_range_start + value - source_range_start
    return value


def transform_seed(seed, maps):
    value = seed
    for map in maps:
        value = transform(value, map)
    return value


def star(filename: str):
    input = list(read_input(filename))
    seeds, *maps = input
    transforms = [transform_seed(seed, maps) for seed in seeds]
    return min(transforms)
