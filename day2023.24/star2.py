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
        yield np.array([values["px"], values["py"], values["pz"]]), np.array(
            [values["vx"], values["vy"], values["vz"]]
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


x = 0
y = 1
z = 2


def p(number, coordinate):
    return input[number][0][coordinate]


def v(number, coordinate):
    return input[number][1][coordinate]


def line_intersect(pa, va, pb, vb):
    tolerance: float = 1e-10
    w = pa - pb
    m = np.array([[va[0], vb[0], w[0]], [va[1], vb[1], w[1]], [va[2], vb[2], w[2]]])

    return abs(np.linalg.det(m)) < tolerance


input = []


def star(filename: str):
    global input
    input = list(read_input(filename))
    # xmin, ymin = 7, 7
    # xmax, ymax = 27, 27
    xmin, ymin = 200000000000000, 200000000000000
    xmax, ymax = 400000000000000, 400000000000000
    number = 0
    for (pa, va), (pb, vb) in itertools.combinations(input, 2):
        if are_vectors_colinear(va, vb):
            print(f"{pa=} {va=} {pb=} {vb=}")

            print("colinear")
        elif line_intersect(pa, va, pb, vb):
            print(f"{pa=} {va=} {pb=} {vb=}")

            print("intersect")

    print(input)
    m = []
    vec = []
    for number in range(len(input)):
        m.append(
            [
                v(number, y),
                -1,
                p(number, x),
                -v(number, x),
                # 1,
                -p(number, y),
                0,
                0,
                0,
                # 0,
            ]
        )
        vec.append(-p(number, y) * v(number, x) + p(number, x) * v(number, y))
        m.append(
            [
                v(number, z),
                0,
                0,
                0,
                # 0,
                -p(number, z),
                -1,
                p(number, x),
                -v(number, x),
                # 1,
            ]
        )
        vec.append(-p(number, z) * v(number, x) + p(number, x) * v(number, z))

    m = np.array(m)
    vec = np.array(vec)

    print(f"{m=}")
    print(f"{vec=}")
    print(f"{m[0:8]=}")

    print(f"{np.linalg.matrix_rank(m)=}")
    print(f"{np.linalg.matrix_rank(m[:8])=}")

    m_inv = np.linalg.inv(m[:8])
    print(f"{np.linalg.det(m[:8])=}")

    result = np.dot(m_inv, vec[:8])
    print(f"{result=}")
    print(f"{result[0],result[3], result[7]=}")

    # print(m.dot(result), vec)

    # equations = []
    # for p, v in input:
    #     equations.append(f"(p1-{p[x]})*({v[y]}-v2) = ({v[x]}-v1)*(p2-{p[y]})")
    #     equations.append(f"(p1-{p[x]})*({v[z]}-v3) = ({v[x]}-v1)*(p3-{p[z]})")
    # print(" , ".join(equations))


# https://www.wolframalpha.com/
# https://www.numberempire.com/equationsolver.php
