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
            if "map" in line:
                continue
            values.append([int(value) for value in line.split()])
        yield values


def transform(seed_range, map):
    if len(map) == 0:
        yield seed_range
        return

    destination_range_start, source_range_start, range_length = map[0]
    start, end = seed_range

    if (
        source_range_start <= start <= source_range_start + range_length - 1
        and source_range_start <= end <= source_range_start + range_length - 1
    ):
        yield (
            destination_range_start + start - source_range_start,
            destination_range_start + end - source_range_start,
        )
        return

    # 1 et 2
    if end < source_range_start or start > source_range_start + range_length - 1:
        yield from transform(seed_range, map[1:])
        return

    if start < source_range_start:
        yield from transform((start, source_range_start - 1), map)
        yield from transform((source_range_start, end), map)
        return

    yield from transform((start, source_range_start + range_length - 1), map)
    yield from transform((source_range_start + range_length - 1 + 1, end), map)


def transform_seed_range(seed_range, maps):
    ranges = [seed_range]
    for map in maps:
        new_ranges = []
        for current_range in ranges:
            new_ranges.extend(list(transform(current_range, map)))
        ranges = new_ranges
    return min(start for start, end in ranges)


def star(filename: str):
    input = list(read_input(filename))
    seeds, *maps = input
    real_seeds = []
    for seed_index in range(0, len(seeds), 2):
        real_seeds.append(
            (seeds[seed_index], seeds[seed_index] + seeds[seed_index + 1] - 1)
        )

    transforms = [transform_seed_range(seed, maps) for seed in real_seeds]
    pprint(transforms)
    return min(transforms)
