from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from pathlib import Path
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile

from utils import read_dicts_from_input, read_lines_from_input, read_words_from_input


def distance(line1: str, line2: str) -> int:
    return sum(1 for c1, c2 in zip(line1, line2) if c1 != c2)


def nearly_equal(lines1: list[str], lines2: list[str]):
    return sum(distance(line1, line2) for line1, line2 in zip(lines1, lines2)) == 1


def get_reflexion_line_with_smudge(lines: list[str]) -> Optional[int]:
    size = len(lines)
    reversed_lines = list(reversed(lines))

    for tested_line in range(1, size // 2 + 1):
        if nearly_equal(
            lines[: tested_line * 1], reversed_lines[-2 * tested_line : -tested_line]
        ):
            return tested_line
        if nearly_equal(
            lines[tested_line * -2 : -tested_line], reversed_lines[: 1 * tested_line]
        ):
            return size - tested_line

    return None


def get_reflexion_line(lines: list[str]) -> Optional[int]:
    size = len(lines)
    reversed_lines = list(reversed(lines))

    for tested_line in range(1, size // 2 + 1):
        if lines[: tested_line * 2] == reversed_lines[-2 * tested_line :]:
            return tested_line
        if lines[tested_line * -2 :] == reversed_lines[: 2 * tested_line]:
            return size - tested_line

    return None


@dataclass
class Pattern:
    rows: list[str]

    def __post_init__(self):
        self.columns = []
        for c in range(len(self.rows[0])):
            self.columns.append("".join(line[c] for line in self.rows))

    def reflexion_points(self):
        reflexion_line = get_reflexion_line_with_smudge(self.rows)

        reflexion_column = get_reflexion_line_with_smudge(self.columns)

        if reflexion_line is not None and reflexion_column is not None:
            raise ValueError

        if reflexion_line is not None:
            return reflexion_line * 100
        return reflexion_column


def read_input(filename: str):
    text = Path(filename).read_text()
    pattern_strings = text.split("\n\n")
    for pattern_string in pattern_strings:
        yield Pattern(pattern_string.split("\n"))


def star(filename: str):
    input = list(read_input(filename))

    return sum(pattern.reflexion_points() for pattern in input)
