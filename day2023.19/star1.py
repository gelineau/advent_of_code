from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile
from grid import Grid
from puzzle import *

from utils import read_dicts_from_input, read_lines_from_input, read_words_from_input


def read_input(filename: str):
    # {x=97,m=3034,a=520,s=1230}

    template = "{{x={x:d},m={m:d},a={a:d},s={s:d}}}"
    for values in read_dicts_from_input(filename, template):
        yield values


def star(filename: str):
    input = list(read_input(filename))
    result = 0
    for line in input:
        try:
            inp(**line)
        except Rejected:
            continue
        except Accepted:
            result += line["x"] + line["m"] + line["a"] + line["s"]

    return result
