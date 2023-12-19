from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile
from grid import Grid

from utils import (
    read_dicts_from_input,
    read_lines_from_input,
    read_words_from_input,
    read_line_groups_from_input,
)


def read_input(filename: str):
    rules_strings, data_string = read_line_groups_from_input(filename)
    rules = []

    template = "{name}{{{steps_string}}}"
    for line in rules_strings:
        parsing_template = compile(template)
        result = parsing_template.parse(line)
        if result is None:
            raise ValueError(f"could not parse `{line}` with template `{template}`")
        steps = []
        for step_string in result.named["steps_string"].split(","):
            if "<" in step_string:
                step_type, rest = step_string.split("<")
                value, call = rest.split(":")
                value = int(value)
                steps.append(("<", step_type, value, call))
            elif ">" in step_string:
                step_type, rest = step_string.split(">")
                value, call = rest.split(":")
                value = int(value)
                steps.append((">", step_type, value, call))
            else:
                steps.append((step_string, None, None, None))
        result.named["steps"] = steps
        rules.append(result.named)

    # for words in read_words_from_input(filename):
    #     yield words
    #
    # template = "{min1:d}-{max1:d},{min2:d}-{max2:d}"
    # for values in read_dicts_from_input(filename, template):
    #     yield values

    return rules


x, m, a, s = 0, 1, 2, 3


def apply_rules(rules, rule_name, intervals):
    print(f"{rule_name=}{intervals=}")
    intervals = deepcopy(intervals)
    rule = rules[rule_name]
    for rule_type, variable, limit, call in rule:
        if rule_type == "A":
            if all(start < end for start, end in intervals):
                yield intervals
                return
            else:
                return
        if rule_type == "R":
            return

        if rule_type == "<":
            variable_index = "xmas".index(variable)
            new_intervals = deepcopy(intervals)
            new_intervals[variable_index][1] = limit
            yield from apply_rules(rules, call, new_intervals)
            intervals[variable_index][0] = limit
            continue

        if rule_type == ">":
            variable_index = "xmas".index(variable)
            new_intervals = deepcopy(intervals)
            new_intervals[variable_index][0] = limit + 1
            yield from apply_rules(rules, call, new_intervals)
            intervals[variable_index][1] = limit + 1
            continue

        else:
            yield from apply_rules(rules, rule_type, intervals)


def interval_size(intervals):
    product = 1
    for start, end in intervals:
        product *= end - start
    return product


def star(filename: str):
    input = list(read_input(filename))
    rules = {}
    for line in input:
        rules[line["name"]] = line["steps"]
    rules["A"] = [("A", None, None, None)]
    rules["R"] = [("R", None, None, None)]

    accepted_intervals = list(apply_rules(rules, "in", [[1, 4001] for _ in range(4)]))

    print("accepted")
    pprint(accepted_intervals)

    return sum(interval_size(interval) for interval in accepted_intervals)

    # rfg [[[1, 2440], [1, 4001], [1, 4001], [537, 4001]]]

    # qkq [[[1, 1416], [1, 4001], [1, 4001], [1, 4001]],
    #  [[2663, 4001], [1, 4001], [1, 4001], [1, 4001]]]
