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
        yield line


def get_digits(line: str):
    for char in line:
        if char.isdigit():
            yield char


def transform_digitswrong(line):
    replacements = (
        ("one", "1"),
        ("two", "2"),
        ("three", "3"),
        ("four", "4"),
        ("five", "5"),
        ("six", "6"),
        ("seven", "7"),
        ("eight", "8"),
        ("nine", "9"),
    )

    indexes = [
        (line.find(number), number, result)
        for number, result in replacements
        if line.find(number) != -1
    ]

    if not indexes:
        return line

    index, string, digit = min(indexes)
    line = line[:index] + digit + line[index + len(string) :]
    # print(indexes)
    # print(line)

    indexes = [
        (line.rfind(number), number, result)
        for number, result in replacements
        if line.rfind(number) != -1
    ]
    # print(indexes)
    if not indexes:
        return line

    index, string, digit = max(indexes)
    line = line[:index] + digit + line[index + len(string) :]
    return line


def transform_digits(line):
    replacements = (
        ("one", "1"),
        ("two", "2"),
        ("three", "3"),
        ("four", "4"),
        ("five", "5"),
        ("six", "6"),
        ("seven", "7"),
        ("eight", "8"),
        ("nine", "9"),
    )

    digit_indexes = [
        (line.find(result), result)
        for number, result in replacements
        if line.find(result) != -1
    ]

    indexes = [
        (line.find(number), result)
        for number, result in replacements
        if line.find(number) != -1
    ]

    indexmin, digitmin = min(indexes + digit_indexes)

    digit_indexes = [
        (line.rfind(result), result)
        for number, result in replacements
        if line.rfind(result) != -1
    ]

    indexes = [
        (line.rfind(number), result)
        for number, result in replacements
        if line.rfind(number) != -1
    ]
    indexmax, digitmax = max(indexes + digit_indexes)

    return digitmin + digitmax


def star(filename: str):
    lines = list(read_input(filename))
    sum = 0
    for line in lines:
        line = transform_digits(line)
        digits = list(get_digits(line))
        number = int(digits[0] + digits[-1])
        print(number)
        sum += number
    return sum
