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
        self.counter_count = len(self.counter)
        self.max_count = max(self.counter.values())
        self.translated = (
            self.card_string.replace("T", "B").replace("K", "R").replace("A", "S")
        )

    def __lt__(self, other):
        if self.max_count > other.max_count:
            return False
        if self.max_count < other.max_count:
            return True

        if self.counter_count > other.counter_count:
            return True
        if self.counter_count < other.counter_count:
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
    result = sum(card.bid * rank for rank, card in enumerate(sorted(input), start=1))
    return result
