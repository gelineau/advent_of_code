from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile


from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile

from utils import read_lines_from_input, read_words_from_input, read_dicts_from_input


@dataclass
class Card:
    number: int
    winning_numbers_string: str

    my_numbers_string: str

    def __post_init__(self):
        number_strings = self.winning_numbers_string.split()
        self.winning_numbers = [int(number) for number in number_strings]
        number_strings = self.my_numbers_string.split()
        self.my_numbers = [int(number) for number in number_strings]

    def value(self):
        sum_value = 0
        for my_number in self.my_numbers:
            if my_number in self.winning_numbers:
                sum_value += 1
        return sum_value


def read_input(filename: str):
    # for line in read_lines_from_input(filename):
    #     yield line
    #
    # for words in read_words_from_input(filename):
    #     yield words
    #
    template = "Card {number:d^}: {winning_numbers_string} | {my_numbers_string}"
    for values in read_dicts_from_input(filename, template, debug=True):
        print(values)
        yield Card(**values)


def star(filename: str):
    cards = list(read_input(filename))
    numbers = [1] * len(cards)

    for i, card in enumerate(cards):
        value = card.value()
        for delta in range(1, value + 1):
            numbers[i + delta] += numbers[i]

    return sum(numbers)
