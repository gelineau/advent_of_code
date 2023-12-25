from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from functools import lru_cache, cache
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


def find_dependent_number(i, supports):
    falling = set()

    while True:
        found = len(falling)
        for j, support in enumerate(supports):
            if j == i:
                continue
            if bricks[j].zmin == 1:
                continue
            if all(s in falling or s == i for s in support):
                falling.add(j)
        if len(falling) == found:
            break
    return falling


def moving_sum():
    supports = []
    for i, supported in enumerate(bricks):
        supports_for_i = []
        for j, brick in enumerate(bricks):
            if brick.supports(supported):
                supports_for_i.append(j)
        supports.append(supports_for_i)

    # disintegrable = len(bricks)
    # for i, brick in enumerate(bricks):
    #     if any(support == [i] for support in supports):
    #         disintegrable -= 1
    print(supports)
    falling = 0
    print(len(bricks))
    print(f"{bricks[0]=}, {bricks[3]=}, {bricks[98 - 74]=}")
    for i in range(len(bricks) + 1):
        print(f"la brique {i} déclenche ", find_dependent_number(i, supports))
        falling += len(find_dependent_number(i, supports))
    return falling


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
                # print(f"falling {i}")
                brick.zmin -= 1
                brick.zmax -= 1
                found = True
        if found == False:
            return


def star(filename: str):
    global bricks
    all_bricks = list(read_input(filename))

    examples = []
    i = 74
    print(i)
    bricks = deepcopy(all_bricks[i:101])
    print(len(bricks))
    fall()
    print(len(bricks))
    s = moving_sum()
    print(s)

    # 1497 too low
    # 2242506 too high
