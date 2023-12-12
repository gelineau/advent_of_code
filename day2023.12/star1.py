from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile

from utils import read_dicts_from_input, read_lines_from_input, read_words_from_input


def read_input(filename: str):
    template = "{puzzle} {numbers}"
    for values in read_dicts_from_input(filename, template):
        yield values["puzzle"], tuple(
            int(number) for number in values["numbers"].split(",")
        )


@lru_cache(None)
def number_possibilities(puzzle: str, numbers: tuple[int]):
    if numbers == ():
        result = int("#" not in set(puzzle))
        # print(puzzle, numbers, result)
        return result
    if puzzle == "":
        if numbers[0] != 0:
            result = 0
            # print(puzzle, numbers, result)
            return result
        result = number_possibilities(puzzle, numbers[1:])
        # print(puzzle, numbers, result)
        return result

    if puzzle == ".":
        result = int(numbers == (0,))
        # print(puzzle, numbers, result)
        return result
    if puzzle == "#":
        result = int(numbers == (1,))
        # print(puzzle, numbers, result)
        return result

    if numbers[0] == 0:
        result = number_possibilities(puzzle, numbers[1:])
        # print(puzzle, numbers, result)
        return result
    p0 = puzzle[0]

    if p0 == ".":
        result = number_possibilities(puzzle[1:], numbers)
        # print(puzzle, numbers, result)
        return result

    if p0 == "#":
        number_hashes = numbers[0]
        if len(puzzle) == number_hashes:
            if "." in set(puzzle):
                result = 0
                # print(puzzle, numbers, result)
                return result
            result = number_possibilities("", numbers[1:])
            # print(puzzle, numbers, result)
            return result

        if len(puzzle) < number_hashes:
            return 0

        if "." in set(puzzle[:number_hashes]):
            result = 0
            # print(puzzle, numbers, result)
            return result
        if puzzle[number_hashes] == "#":
            result = 0
            # print(puzzle, numbers, result)
            return result
        result = number_possibilities(puzzle[number_hashes + 1 :], numbers[1:])
        # print(puzzle, numbers, result)
        return result

    # p0 == "?"
    result = number_possibilities("#" + puzzle[1:], numbers) + number_possibilities(
        "." + puzzle[1:], numbers
    )
    # print(puzzle, numbers, result)
    return result


def transform_line(line):
    return line


def star(filename: str):
    input = list(read_input(filename))

    for line in input:
        print(line)
        transformed_line = transform_line(line)
        print(number_possibilities(*transformed_line))
    return sum(number_possibilities(*transform_line(line)) for line in input)
