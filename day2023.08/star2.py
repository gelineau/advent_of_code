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
    for line in lines:
        network[line[:3]] = line[7:10], line[12:15]
    return network


network = {}


@lru_cache(None)
def make_one_complete_turn(node, instructions):
    ends = set()
    for turn, instuction in enumerate(instructions, start=1):
        left, right = network[node]
        if instuction == "L":
            node = left
        elif instuction == "R":
            node = right
        else:
            raise ValueError
        if node.endswith("Z"):
            ends.add(turn)
    return node, ends


def star_bruteforce(filename: str):
    input = list(read_input(filename))
    instructions = input[0].strip()
    print(instructions)

    create_network(input[2:])
    # pprint(network)
    nodes = [node for node in network if node.endswith(("A"))]

    for turn, instuction in enumerate(cycle(instructions), start=1):
        next_nodes = [network[node] for node in nodes]
        nodes = []
        for left, right in next_nodes:
            if instuction == "L":
                nodes.append(left)
            elif instuction == "R":
                nodes.append(right)
            else:
                raise ValueError
        # print(nodes)
        if all(node.endswith("Z") for node in nodes):
            return turn


size = 1000000


@lru_cache(None)
def make_big_turn(node, instructions):
    turn = 0
    final_turns = []
    for step in range(size):
        node, winning_turns = make_one_complete_turn(node, instructions)
        final_turns.extend([turn + winning_turn for winning_turn in winning_turns])

        turn += len(instructions)
    return node, set(final_turns)


def star(filename: str):
    input = list(read_input(filename))
    instructions = input[0].strip()
    print(instructions)

    network = create_network(input[2:])
    # pprint(network)
    nodes = [node for node in network if node.endswith(("A"))]

    turn = 0
    step = 0
    while True:
        results = [make_big_turn(node, instructions) for node in nodes]
        # print(results)
        nodes = [result[0] for result in results]
        winning_turns = set.intersection(*(result[1] for result in results))
        if winning_turns:
            return turn + min(winning_turns)

        turn += size * len(instructions)
        step += 1
        if step % 1 == 0:
            print(step)
