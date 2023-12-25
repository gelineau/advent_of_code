from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile
from grid import Grid

from utils import read_dicts_from_input, read_lines_from_input, read_words_from_input


@dataclass
class Brick:
    xmin: int
    ymin: int
    zmin: int
    xmax: int
    ymax: int
    zmax: int

    def can_fall(self, i):
        if self.zmin == 1:
            return False

        for brick in bricks:
            if brick.supports(self):
                return False
        return True

    def supports(self, other):
        if other.zmin - 1 != self.zmax:
            return False
        if (
            (other.xmin <= self.xmin <= other.xmax)
            or (self.xmin <= other.xmin <= self.xmax)
        ) and (
            (other.ymin <= self.ymin <= other.ymax)
            or (self.ymin <= other.ymin <= self.ymax)
        ):
            return True
        return False


def calculate_disintegration():
    supports = []
    for i, supported in enumerate(bricks):
        if i == 3:
            print(3)
        supports_for_i = []
        for j, brick in enumerate(bricks):
            if brick.supports(supported):
                supports_for_i.append(j)
        supports.append(supports_for_i)

    pprint(supports)
    disintegrable = len(bricks)
    for i, brick in enumerate(bricks):
        if any(support == [i] for support in supports):
            disintegrable -= 1

    return disintegrable


def read_input(filename: str):
    template = "{xmin:d},{ymin:d},{zmin:d}~{xmax:d},{ymax:d},{zmax:d}"
    for values in read_dicts_from_input(filename, template):
        yield Brick(**values)


bricks = []


def fall():
    while True:
        found = False

        for i, brick in enumerate(bricks):
            if brick.can_fall(i):
                # print(f"falling {'ABCDEFGHIJ'[i]}")
                print("falling {i}")
                brick.zmin -= 1
                brick.zmax -= 1
                found = True
        if found == False:
            return


def star(filename: str):
    global bricks
    bricks = list(read_input(filename))

    fall()
    pprint(bricks)

    return calculate_disintegration()
