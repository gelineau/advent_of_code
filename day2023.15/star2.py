from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile

from utils import (
    read_dicts_from_input,
    read_lines_from_input,
    read_words_from_input,
    read_text_from_input,
)


def read_input(filename: str):
    line = read_text_from_input(filename)

    words = line.split(",")
    for word in words:
        if word.endswith("-"):
            yield "-", word[:-1], 0
        else:
            part1, part2 = word.split("=")
            yield "=", part1, int(part2)


def calculate_hash(word):
    result = 0
    for char in word:
        result += ord(char)
        result *= 17
        result = result % 256
    return result


def find_lens_in_box(box: list[tuple[str, int]], label):
    for place, (place_label, _) in enumerate(box):
        if place_label == label:
            return place
    return None


def remove_from_box(box: list[tuple[str, int]], label):
    return [
        (place_label, place_lens)
        for place_label, place_lens in box
        if place_label != label
    ]


def focusing_power(box: list[tuple[str, int]], box_number):
    return sum(
        (box_number + 1) * (slot + 1) * place_lens
        for slot, (place_label, place_lens) in enumerate(box)
    )


def star(filename: str):
    input = list(read_input(filename))

    boxes: list[list[tuple[str, int]]] = [[] for _ in range(256)]

    for type, label, focal in input:
        print("*" * 50)
        print(type, label, focal)

        box_number = calculate_hash(label)
        print(f"{box_number=}")
        if type == "=":
            place = find_lens_in_box(boxes[box_number], label)
            if place is not None:
                boxes[box_number][place] = label, focal
            else:
                boxes[box_number].append((label, focal))
        elif type == "-":
            boxes[box_number] = remove_from_box(boxes[box_number], label)

    pprint(boxes)
    return sum(focusing_power(box, box_number) for box_number, box in enumerate(boxes))
