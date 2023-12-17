from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from pprint import pprint
from typing import Iterator, List, Optional, Any

import networkx
from parse import compile

from utils import read_dicts_from_input, read_lines_from_input, read_words_from_input


class Grid:
    def __init__(self, input: list[str]):
        self.values = [[int(char) for char in line] for line in input]

    def row_max(self):
        return len(self.values)

    def col_max(self):
        return len(self.values[0])

    def is_in_grid(self, row, column):
        if row < 0 or column < 0 or row >= self.row_max() or column >= self.col_max():
            return False
        return True

    def get(self, row: int, column: int) -> int:
        if self.is_in_grid(row, column):
            return self.values[row][column]
        raise IndexError

    def __repr__(self):
        result = "\n"
        for row in range(self.row_max()):
            result += (
                "".join(str(self.get(row, column)) for column in range(self.col_max()))
                + "\n"
            )

        return result


def read_input(filename: str):
    for line in read_lines_from_input(filename):
        yield line


moves = ">^v<"


def delta(move):
    if move == "<":
        return 0, -1
    if move == ">":
        return 0, 1
    if move == "v":
        return 1, 0
    if move == "^":
        return -1, 0
    raise ValueError


possible_pasts = []
for move in moves:
    possible_pasts.extend(move * n for n in range(1, 11))

print(possible_pasts)


def gest_past_id(past):
    id = possible_pasts.index(past)
    if id == -1:
        raise ValueError
    return id


factor = 100_000


def to_id(row, column, past):
    result = row * factor * factor + column * factor + gest_past_id(past)
    return result


def from_id(id):
    row = id // (factor * factor)
    rest = id % (factor * factor)

    col = rest // factor

    return row, col


origin_id = factor * factor * factor
destination_id = factor * factor * factor + 1


# def from_id(id):
#     return id // y_max, id % y_max
#
#
#
# graph = networkx.Graph()
# for x in range(x_max):
#     for y in range(y_max):
#         if x > 0:
#             graph.add_edge(to_id(x - 1, y), to_id(x, y))
#         if y > 0:
#             graph.add_edge(to_id(x, y - 1), to_id(x, y))
#         graph.add_node(to_id(x, y))
#
#
# origin = to_id(0, 0)
# destination = to_id(x_max - 1, y_max - 1)
#
#
# def cost(origin_id, destination_id, edge_parameters):
#     x, y = from_id(destination_id)
#     return risks[y][x]
#
#
# shortest_path = networkx.dijkstra_path(graph, origin, destination, cost)
# pprint([(from_id(node), cost(None, node, None)) for node in shortest_path])
#
# print(sum(cost(None, node_id, None) for node_id in shortest_path[1:]))


def cost(grid, id1, id2):
    if id2 == destination_id:
        return 0
    if id2 == origin_id:
        return 100000000000000000000000
    row, col = from_id(id2)
    # print(f"calculating cost for {id1=} {id2=} {row=} {col=}")

    return grid.get(row, col)


def turns(move):
    if move == ">" or move == "<":
        return ("v", "^")
    return (">", "<")


def move_one_step(grid, row, col, move):
    drow, dcolumn = delta(move)
    new_row = row + drow
    new_col = col + dcolumn

    if grid.is_in_grid(new_row, new_col):
        return new_row, new_col
    raise IndexError


def calculate_next_states(grid, row, col, past):
    # print(f"calculating next states for {row=} {col=} {past=}")
    if len(past) < 10:
        move = past[-1]
        try:
            next_row, next_column = move_one_step(grid, row, col, move)
            # print(f"{next_row=} {next_column=} {past+move=}")
            yield next_row, next_column, past + move
        except IndexError:
            pass

    if len(past) >= 4:
        for move in turns(past[-1]):
            try:
                next_row, next_column = move_one_step(grid, row, col, move)
                # print(f"{next_row=} {next_column=} {move=}")

                yield next_row, next_column, move
            except IndexError:
                pass


def star(filename: str):
    input = list(read_input(filename))
    grid = Grid(input)

    network_cost = lambda id1, id2, edge_parameter: cost(grid, id1, id2)

    graph = networkx.DiGraph()
    graph.add_node(origin_id)
    graph.add_node(destination_id)

    for row in range(grid.row_max()):
        for col in range(grid.col_max()):
            for past in possible_pasts:
                graph.add_node(to_id(row, col, past))
                # assert (row, col) == from_id(to_id(row, col, past))

    for past in possible_pasts:
        if len(past) >= 4:
            graph.add_edge(
                to_id(grid.row_max() - 1, grid.col_max() - 1, past), destination_id
            )

    graph.add_edge(origin_id, to_id(0, 1, ">"))
    graph.add_edge(origin_id, to_id(1, 0, "v"))

    for row in range(grid.row_max()):
        for col in range(grid.col_max()):
            for past in possible_pasts:
                for next_row, next_col, next_past in calculate_next_states(
                    grid, row, col, past
                ):
                    graph.add_edge(
                        to_id(row, col, past), to_id(next_row, next_col, next_past)
                    )

    shortest_path = networkx.dijkstra_path(
        graph, origin_id, destination_id, network_cost
    )
    pprint([from_id(node) for node in shortest_path])

    print(sum(cost(grid, None, node_id) for node_id in shortest_path[1:]))

    # 1064 too low
