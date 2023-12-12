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
        yield [int(value) for value in line.split()]


def star(filename: str):
    input = list(read_input(filename))
    result_sum = 0
    for input_line in input:
        all_differences = [input_line]
        while set(all_differences[-1]) != {0}:
            last_differences = all_differences[-1]
            differences = [
                v2 - v1 for v1, v2 in zip(last_differences, last_differences[1:])
            ]
            all_differences.append(differences)

        for i in range(len(all_differences) - 2, -1, -1):
            all_differences[i].append(
                all_differences[i][-1] + all_differences[i + 1][-1]
            )

        print(all_differences[0][-1])
        result_sum += all_differences[0][-1]

    return result_sum
