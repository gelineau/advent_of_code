from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat, cycle
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile

from utils import read_dicts_from_input, read_lines_from_input, read_words_from_input


def read_input(filename: str):
    for line in read_lines_from_input(filename):
        yield line


def create_network(lines):
    network = {}
    for line in lines:
        network[line[:3]] = line[7:10], line[12:15]
    return network


def star(filename: str):
    input = list(read_input(filename))
    instructions = input[0].strip()
    print(instructions)

    network = create_network(input[2:])
    pprint(network)
    node = "AAA"

    for turn, instuction in enumerate(cycle(instructions), start=1):
        left, right = network[node]
        if instuction == "L":
            node = left
        elif instuction == "R":
            node = right
        else:
            raise ValueError
        if node == "ZZZ":
            return turn
