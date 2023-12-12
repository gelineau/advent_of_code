from collections import Counter
from dataclasses import dataclass
from functools import lru_cache, total_ordering
from itertools import repeat
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile

from utils import read_dicts_from_input, read_lines_from_input, read_words_from_input


@total_ordering
@dataclass
class Card:
    # A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2
    card_string: str
    bid: int = 1

    def __post_init__(self):
        self.counter = Counter(self.card_string)
        self.values = sorted(value for key, value in self.counter.items() if key != "J")
        self.jokers = self.counter["J"]
        self.max = max(self.values, default=0) + self.jokers
        if len([1 for value in self.values if value == 2]) == 2 and self.jokers == 0:
            self.max = 2.5
        if len([1 for value in self.values if value == 2]) == 2 and self.jokers == 1:
            self.max = 3.5
        if 2 in self.values and 3 in self.values and self.jokers == 0:
            self.max = 3.5

        self.translated = (
            self.card_string.replace("T", "B")
            .replace("K", "R")
            .replace("A", "S")
            .replace("J", "1")
        )

    def __lt__(self, other):
        if self.max < other.max:
            return True
        if self.max > other.max:
            return False

        if self.translated < other.translated:
            return True

        return False


def read_input(filename: str):
    # for line in read_lines_from_input(filename):
    #     yield line

    # for words in read_words_from_input(filename):
    #     yield words
    #
    template = "{card_string} {bid:d}"
    for values in read_dicts_from_input(filename, template):
        yield Card(**values)


def star(filename: str):
    input = list(read_input(filename))
    # pprint(sorted(input))
    result = sum(card.bid * rank for rank, card in enumerate(sorted(input), start=1))
    return result

    # 243889817 too low
    # 244068822 too low
    # 244365572 wrong
    # 244848487
