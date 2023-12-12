from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile

from utils import read_dicts_from_input, read_lines_from_input, read_words_from_input


def read_input(filename: str):
    # for line in read_lines_from_input(filename):
    #     yield line
    #
    # for words in read_words_from_input(filename):
    #     yield words

    template = "Game {number:d}: {turns}"
    for values in read_dicts_from_input(filename, template):
        number = values["number"]
        yield number, values["turns"].split(";")


def star(filename: str):
    input = list(read_input(filename))
    games = []
    for game_number, turn_strings in input:
        turns = []
        for turn_string in turn_strings:
            turn = Counter()
            color_strings = turn_string.split(",")
            for color_string in color_strings:
                number, color = color_string.split()
                number = int(number)
                turn[color] = number
            turns.append(turn)
        games.append((game_number, turns))

    pprint(games)
    max_colors = {"blue": 14, "green": 13, "red": 12}

    sum_powers = 0
    for number, turns in games:
        max_game_colors = Counter()
        for color in max_colors:
            max_color = max(turn[color] for turn in turns)
            max_game_colors[color] = max_color
        # print(f"{number=} {max_colors=}")
        power = (
            max_game_colors["green"] * max_game_colors["blue"] * max_game_colors["red"]
        )
        sum_powers += power
    return sum_powers
