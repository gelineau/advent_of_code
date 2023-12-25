import sys
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from pprint import pprint
from typing import Iterator, List, Optional, Any, Iterable

import networkx
from parse import compile

from utils import read_dicts_from_input, read_lines_from_input, read_words_from_input


class Grid:
    def __init__(self, input: Iterable[str]):
        self.values = [[char for char in line] for line in input]
        self.start_col = [
            col for col, value in enumerate(self.values[0]) if value == "."
        ][0]
        print(f"{self.start_col=}")
        self.end_col = [
            col for col, value in enumerate(self.values[-1]) if value == "."
        ][0]

    def row_max(self):
        return len(self.values)

    def col_max(self):
        return len(self.values[0])

    def is_in_grid(self, row, column):
        if row < 0 or column < 0 or row >= self.row_max() or column >= self.col_max():
            return False
        return True

    def get(self, row: int, column: int) -> str:
        if self.is_in_grid(row, column):
            return self.values[row][column]
        raise IndexError

    def set(self, row: int, col: int, color: str):
        if not self.is_in_grid(row, col):
            raise IndexError
        self.values[row][col] = color

    def get_point_repr(self, row, col, path):
        if (row, col) in path:
            return "O"
        if row == 0 and col == self.start_col:
            return "S"
        return self.get(row, col)

    def display(self, path=()):
        result = "\n"
        for row in range(self.row_max()):
            result += (
                "".join(
                    self.get_point_repr(row, column, path)
                    for column in range(self.col_max())
                )
                + "\n"
            )

        print(result)

    def neighbours(self, row, col):
        for direction in "UDLR":
            drow, dcol = delta(direction)
            if self.is_in_grid(row + drow, col + dcol):
                yield row + drow, col + dcol

    def empty_neighbours(self, row, col):
        for neighbour in self.neighbours(row, col):
            if self.get(*neighbour) == ".":
                yield neighbour
            elif self.get(*neighbour) == "#":
                continue
            # elif add((row, col), delta(self.get(*neighbour))) == neighbour:
            else:
                yield neighbour

    def is_cross(self, row, col):
        return self.is_empty(row, col) and (
            len(list(self.empty_neighbours(row, col))) in [1, 3, 4]
        )

    def simplify(self):
        nodes = [
            (row, col)
            for row in range(self.row_max())
            for col in range(self.col_max())
            if self.is_cross(row, col)
        ]
        edges = set()

        for node in nodes:
            for immediate_neighbour in self.empty_neighbours(*node):
                neighbour = immediate_neighbour
                previous = node
                cost = 1
                while not self.is_cross(*neighbour):
                    assert (
                        len(
                            [
                                n
                                for n in self.empty_neighbours(*neighbour)
                                if n != previous
                            ]
                        )
                        == 1
                    ), f"{neighbour=} {self.is_cross(*neighbour)=} {list(self.empty_neighbours(*neighbour))=}"
                    previous, neighbour = (
                        neighbour,
                        [n for n in self.empty_neighbours(*neighbour) if n != previous][
                            0
                        ],
                    )
                    cost += 1

                edges.add(tuple(sorted((node, neighbour))) + (cost,))

        return [self.to_id(*node) for node in nodes], [
            (self.to_id(*origin), self.to_id(*destination), cost)
            for (origin, destination, cost) in edges
        ]

    def is_empty(self, n_row, n_col):
        if not self.is_in_grid(n_row, n_col):
            return False
        if self.get(n_row, n_col) == "#":
            return False
        return True

    def one_direction_neighbours(self, row, col):
        for direction in "DR":
            drow, dcol = delta(direction)
            n_row, n_col = row + drow, col + dcol
            if self.is_empty(n_row, n_col):
                yield n_row, n_col

    def get_all_edges(self):
        for row, col in self.get_all_vertices():
            for neighbour in self.one_direction_neighbours(row, col):
                yield (row, col), neighbour

    def get_all_vertices(self):
        for row in range(self.row_max()):
            for col in range(self.col_max()):
                if self.is_empty(row, col):
                    yield row, col

    def get_paths(self, path_so_far, start):
        # print()
        # self.display(path_so_far)
        for neighbour in self.empty_neighbours(*start):
            if neighbour in path_so_far:
                continue
            new_path = deepcopy(path_so_far)
            new_path.add(neighbour)
            if neighbour[0] == self.row_max() - 1:
                yield path_so_far
            else:
                yield from self.get_paths(new_path, neighbour)

    def to_id(self, row, col):
        return row * 1000_000 + col


def add(point1, point2):
    return (point1[0] + point2[0], point1[1] + point2[1])


def delta(move):
    if move == "L" or move == "<":
        return 0, -1
    if move == "R" or move == ">":
        return 0, 1
    if move == "D" or move == "v":
        return 1, 0
    if move == "U" or move == "^":
        return -1, 0
    raise ValueError(move)


def read_input(filename: str):
    return Grid(read_lines_from_input(filename))


def star(filename: str):
    sys.setrecursionlimit(10000)

    grid = read_input(filename)
    grid.display()
    # return max(
    #     [
    #         len(path)
    #         for path in grid.get_paths({(0, grid.start_col)}, (0, grid.start_col))
    #     ]
    # )

    print(f"{grid.is_cross(0,1)=} {list(grid.empty_neighbours(0,1))=}")
    graph = networkx.Graph()
    vertices, edges = grid.simplify()
    costs = {}
    pprint(edges)
    pprint(vertices)

    for vertex in vertices:
        graph.add_node(vertex)

    for origin, destination, cost in edges:
        costs[(origin, destination)] = cost
        costs[(destination, origin)] = cost
        graph.add_edge(origin, destination)

    origin = grid.to_id(0, grid.start_col)
    destination = grid.to_id(grid.row_max() - 1, grid.end_col)

    print(origin, destination)
    max_so_far = 0
    for i, path in enumerate(networkx.all_simple_paths(graph, origin, destination)):
        path_cost = sum(
            costs[(origin, destination)] for origin, destination in zip(path, path[1:])
        )
        max_so_far = max(path_cost, max_so_far)
        if i % 10000 == 0:
            print(f"{i=} {max_so_far=}")

    return max_so_far

    # 6398 too low
    # 6410 too low
