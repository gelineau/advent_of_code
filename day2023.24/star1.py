import itertools
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile
from grid import Grid
import numpy as np

from utils import read_dicts_from_input, read_lines_from_input, read_words_from_input


def read_input(filename: str):
    # 19, 13, 30 @ -2, 1, -2
    template = "{px:d}, {py:d}, {pz:d} @ {vx:d}, {vy:d}, {vz:d}"
    for values in read_dicts_from_input(filename, template):
        yield np.array([values["px"], values["py"]]), np.array(
            [values["vx"], values["vy"]]
        )


def are_vectors_colinear(
    v1: np.ndarray, v2: np.ndarray, tolerance: float = 1e-10
) -> bool:
    # Check if the cross product is nearly zero (within a specified tolerance)
    cross_product_magnitude = np.linalg.norm(np.cross(v1, v2))
    return np.isclose(cross_product_magnitude, 0, atol=tolerance).all()


def intersection(
    pa: np.ndarray, va: np.ndarray, pb: np.ndarray, vb: np.ndarray
) -> Optional[np.ndarray]:
    # Extract components of points and vectors
    xa, ya = pa
    xb, yb = pb
    vxa, vya = va
    vxb, vyb = vb

    # # Solve the system of equations to find t and s
    # t = (ya - yb + vya * (xb - xa) / vxa) / (vyb - vxb * vya / vxa)
    # s = (yb - ya + vyb * t) / vya

    m = np.array([[vxa, vxb], [vya, vyb]])
    m_inv = np.linalg.inv(m)

    result = np.dot(m_inv, (pa - pb))
    s = -result[0]
    t = result[1]

    print(s, t)
    if t < 0 or s < 0:
        return None

    intersection_point = np.array([xa + vxa * s, ya + vya * s])
    return intersection_point


def star(filename: str):
    input = list(read_input(filename))
    # xmin, ymin = 7, 7
    # xmax, ymax = 27, 27
    xmin, ymin = 200000000000000, 200000000000000
    xmax, ymax = 400000000000000, 400000000000000
    number = 0
    for (pa, va), (pb, vb) in itertools.combinations(input, 2):
        print(f"{pa=} {va=} {pb=} {vb=}")
        if are_vectors_colinear(va, vb):
            continue
        else:
            intersection_point = intersection(pa, va, pb, vb)
            if intersection_point is None:
                continue
            if (
                xmin <= intersection_point[0] <= xmax
                and ymin <= intersection_point[1] <= ymax
            ):
                number += 1
    return number
