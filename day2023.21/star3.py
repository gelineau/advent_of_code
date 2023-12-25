import pickle
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import lru_cache, cache
from itertools import repeat
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile

from utils import read_dicts_from_input, read_lines_from_input, read_words_from_input


from typing import Iterable


class Grid:
    def __init__(self, input: Iterable[str]):
        self.values = [[char for char in line] for line in input]

        for row in range(self.row_max()):
            for col in range(self.col_max()):
                if self.get(row, col) == "S":
                    self.start = (row, col)

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

    def print_positions(self, positions):
        print("\n")
        for row in range(self.row_max()):
            print(
                "".join(
                    str(self.get(row, column))
                    if (row, column) not in positions
                    else "O"
                    for column in range(self.col_max())
                )
            )

    def neighbours(self, row, col):
        for direction in "UDLR":
            drow, dcol = delta(direction)
            if self.is_in_grid(row + drow, col + dcol):
                yield row + drow, col + dcol

    # def find_empty_neighbours(self, position):
    #     for neighbour in self.neighbours(*position):
    #         if self.get(*neighbour) in [".", "S"]:
    #             yield neighbour

    def find_empty_neighbours(self, position):
        for direction in "UDLR":
            new_position = list(add(delta(direction), position))

            if new_position[0] < 0:
                row_grid = -1
                new_position[0] += self.row_max()
            elif new_position[0] >= self.row_max():
                row_grid = +1
                new_position[0] -= self.row_max()
            else:
                row_grid = 0

            if new_position[1] < 0:
                col_grid = -1
                new_position[1] += self.col_max()
            elif new_position[1] >= self.col_max():
                col_grid = +1
                new_position[1] -= self.col_max()
            else:
                col_grid = 0

            if self.get(*new_position) in [".", "S"]:
                yield (row_grid, col_grid), tuple(new_position)


def delta(move):
    if move == "L":
        return 0, -1
    if move == "R":
        return 0, 1
    if move == "D":
        return 1, 0
    if move == "U":
        return -1, 0
    raise ValueError


def read_input(filename: str):
    grid = Grid(read_lines_from_input(filename))
    print(grid)
    return grid


def add(grid_position, new_grid_position):
    return (
        grid_position[0] + new_grid_position[0],
        grid_position[1] + new_grid_position[1],
    )


@dataclass(unsafe_hash=True)
class State:
    positions: dict[tuple[int, int], set[tuple[int, int]]]
    full_positions: dict[tuple[int, int], int]
    min_row: int
    max_row: int
    min_col: int
    max_col: int

    def count(self):
        return count(self.positions) + sum(self.full_positions.values())


def move_state(state: State):
    new_positions = defaultdict(set)

    for cell_position, positions in state.positions.items():
        for position in positions:
            for new_relative_cell_position, new_relative_positions in move_steps(
                position, 1
            ).items():
                absolute_position = add(cell_position, new_relative_cell_position)
                if absolute_position not in state.full_positions:
                    new_positions[absolute_position] = new_positions[
                        absolute_position
                    ].union(new_relative_positions)

    for row in range(state.min_row - 1, state.max_row + 2):
        for col in range(state.min_col - 1, state.max_col + 2):
            if (row, col) in state.full_positions:
                continue

            for move in "URDL":
                drow, dcolumn = delta(move)
                neighbour_cell = add((row, col), (drow, dcolumn))
                if neighbour_cell in state.full_positions:
                    if state.full_positions[neighbour_cell] == number_1:
                        neighbour_positions = new_positions_for_number_1
                    else:
                        neighbour_positions = new_positions_for_number_2

                    # print(f"adding to ({row=} {col=})")
                    # pprint(neighbour_positions[(-drow, -dcolumn)])
                    new_positions[(row, col)] = new_positions[(row, col)].union(
                        neighbour_positions[(-drow, -dcolumn)]
                    )

    for cell, number in state.full_positions.items():
        if number == number_1:
            number = number_2
        else:
            number = number_1
        state.full_positions[cell] = number

    final_positions = {}
    for cell, positions in new_positions.items():
        state.min_row = min(state.min_row, cell[0])
        state.max_row = max(state.max_row, cell[0])
        state.min_col = min(state.min_col, cell[1])
        state.max_col = max(state.max_col, cell[1])

        # print(f"{cell=} {len(positions)=} {number_1=} {number_2=}")
        if len(positions) in [number_1, number_2]:
            state.full_positions[cell] = len(positions)
        else:
            final_positions[cell] = positions

    return State(
        final_positions,
        state.full_positions,
        state.min_row,
        state.max_row,
        state.min_col,
        state.max_col,
    )


@cache
def move_steps(position, n):
    if n == 0:
        return {(0, 0): {position}}

    all_positions = defaultdict(set)
    if n == 1:
        inside_position = position
        new_positions = find_neighbours(inside_position)
        for new_grid_position, new_inside_position in new_positions:
            all_positions[new_grid_position].add(new_inside_position)
        return all_positions

    for bunch in [
        1000_000,
        100_000,
        1000,
        580,
        550,
        530,
        500,
        460,
        420,
        400,
        370,
        350,
        330,
        300,
        290,
        270,
        250,
        230,
        200,
        180,
        150,
        120,
        100,
        70,
        50,
        25,
        20,
        10,
        4,
        2,
        1,
    ]:
        if n > bunch:
            for grid_position, inside_positions in move_steps(position, bunch).items():
                for inside_position in inside_positions:
                    new_positions = move_steps(inside_position, n - bunch)
                    for (
                        new_grid_position,
                        new_inside_positions,
                    ) in new_positions.items():
                        for new_inside_position in new_inside_positions:
                            all_positions[add(grid_position, new_grid_position)].add(
                                new_inside_position
                            )

            return all_positions


@cache
def find_neighbours(position):
    return tuple(grid.find_empty_neighbours(position))


# def move_one_step(grid, positions):
#     all_positions = set()
#
#     for grid_position, inside_position in positions:
#         new_positions = grid.find_empty_neighbours(inside_position)
#         for new_grid_position, new_inside_position in new_positions:
#             all_positions.add(
#                 (add(grid_position, new_grid_position), new_inside_position)
#             )
#     return all_positions


def count(positions):
    result = 0
    for grid_position, new_positions in positions.items():
        result += len(new_positions)
    return result


grid = None

number_1 = None
number_2 = None

# # puzzle.txt
index_for_number_1 = 139
index_for_number_2 = 140

# puzzle_test.txt
# index_for_number_1 = 19
# index_for_number_2 = 20

new_positions_for_number_1 = None
new_positions_for_number_2 = None


def count0(positions):
    return count({(0, 0): positions[(0, 0)]})


def count_one_grid(grid_position, positions):
    return count({grid_position: positions.get(grid_position, set())})


def calculate_new_positions(positions1):
    new_positions = defaultdict(set)

    for position in positions1[0, 0]:
        for grid_position, next_positions in move_steps(position, 1).items():
            if grid_position != (0, 0):
                new_positions[grid_position] = new_positions[grid_position].union(
                    next_positions
                )
    return new_positions


def star(filename: str):
    global grid
    global new_positions_for_number_2
    global new_positions_for_number_1
    global number_2
    global number_1

    grid = read_input(filename)

    start_position = grid.start

    sys.setrecursionlimit(1000)

    # positions1 = move_steps(start_position, index_for_number_1)
    # new_positions_for_number_1 = calculate_new_positions(positions1)
    # number_1 = count0(positions1)
    #
    # positions2 = move_steps(start_position, index_for_number_2)
    # new_positions_for_number_2 = calculate_new_positions(positions2)
    # number_2 = count0(positions2)
    #
    # pprint(new_positions_for_number_1)
    # pprint(new_positions_for_number_2)
    #
    # print(f"{number_1=} {number_2=}")

    ######################################################

    old_rows_sums = []
    old_sum = 0
    old_sum1 = 0
    # for step in range(1000):
    #     positions = move_steps(start_position, step)
    #     print(f"{step=}, {count(positions)=}")
    #     # for cell in sorted(positions.keys()):
    #     #     print(cell, count_one_grid(cell, positions), end=", ")
    #
    #     row_nb = len({cell[0] for cell in positions if cell[1] == 0})
    #     print(f"{row_nb=}")
    #     assert step < 50 or row_nb == 1 + (step // 11) * 2

    # cols_of_row0 = sorted(cell[1] for cell in positions if cell[0] == 0)
    #
    # sum_except_row0 = sum(len(p) for cell, p in positions.items() if cell[0] != 0)
    # sum_row0 = sum(len(p) for cell, p in positions.items() if cell[0] == 0)
    # print(f"{sum_row0-old_sum=}")
    # old_sum = sum_row0
    # print(f"{sum_row0=}")
    #
    # sum_row1 = sum(len(p) for cell, p in positions.items() if cell[0] == 1)
    # print(f"{sum_row1-old_sum1=}")
    # old_sum1 = sum_row1

    #######################
    # test_row = -2
    #
    # cols_of_row = sorted(cell[1] for cell in positions if cell[0] == test_row)
    # numbers_of_row = [len(positions[(test_row, col)]) for col in cols_of_row]
    #
    # number_of_number1 = len(
    #     [number for number in numbers_of_row if number == number_1]
    # )
    # number_of_number2 = len(
    #     [number for number in numbers_of_row if number == number_2]
    # )
    #
    # sum_of_others = sum(
    #     [number for number in numbers_of_row if number not in [number_1, number_2]]
    # )
    # print(f"{step=} {number_of_number1=} {number_of_number2=} {sum_of_others=}")
    #
    # print(f"{sum(numbers_of_row)-old_sum=}")
    # old_sum = sum(numbers_of_row)
    ###############

    # rows = sorted({cell[0] for cell in positions if cell[1] == 0})
    # rows_sums = [sum(len(positions[row, col]) for col in rows) for row in rows]
    # if len(rows_sums) != len(old_rows_sums):
    #     old_rows_sums = [0] + old_rows_sums
    # print([a - b for a, b in zip(rows_sums, old_rows_sums)])
    # old_rows_sums = rows_sums
    # print(f"{sum(rows_sums)=} {rows_sums=}")
    # cols0 = sorted(cell[1] for cell in positions if cell[0] == 2)[:4]
    # print([(col, len(positions[(2, col)])) for col in cols0])

    # test_row = 10
    # cols_of_row = sorted(cell[1] for cell in positions if cell[0] == test_row)
    # numbers_of_row = [len(positions[(test_row, col)]) for col in cols_of_row]
    # not_full_numbers = [
    #     number for number in numbers_of_row if number not in [number_1, number_2]
    # ]
    # print(sum(not_full_numbers), f"{not_full_numbers=}")
    #
    # test_row = 4
    # cols_of_row = sorted(cell[1] for cell in positions if cell[0] == test_row)
    # numbers_of_row = [len(positions[(test_row, col)]) for col in cols_of_row]
    # not_full_numbers = [
    #     number for number in numbers_of_row if number not in [number_1, number_2]
    # ]
    # print(sum(not_full_numbers), f"{not_full_numbers=}")
    #
    # test_row = 1
    # cols_of_row = sorted(cell[1] for cell in positions if cell[0] == test_row)
    # numbers_of_row = [len(positions[(test_row, col)]) for col in cols_of_row]
    # not_full_numbers = [
    #     number for number in numbers_of_row if number not in [number_1, number_2]
    # ]
    # print(sum(not_full_numbers), f"{not_full_numbers=}")

    # # pprint(sorted([(cell, len(p)) for cell, p in positions.items()]))
    # print(sorted(positions[(0, -2)]))
    #
    # state = State({(0, 0): {start_position}}, {}, 0, 0, 0, 0)
    #
    # for step in range(1, 5005):
    #     state = move_state(state)
    #
    #     print(
    #         step,
    #         state.count(),
    #         state.min_col,
    #         state.max_col,
    #         state.min_row,
    #         state.max_row,
    #         len(state.positions),
    #         len(state.full_positions),
    #     )
    #
    #     if step in [6, 10, 50, 100, 500, 1000, 5000]:
    #         print(f"{state.count()=}")
    #
    # # pprint(sorted([(cell, len(p)) for cell, p in state.positions.items()]))
    # print(sorted(state.positions[(0, -2)]))

    ###############################

    # print(f"{number_1=} {number_2=}")
    # old_rows_sums = []
    # old_sum = [0, 0, 0, 0, 0]
    # diffs = [[], [], [], [], []]
    # for step in range(100):
    #     positions = move_steps(start_position, step)
    #     print(f"{step=}, {count(positions)=}")
    #     # for cell in sorted(positions.keys()):
    #     #     print(cell, count_one_grid(cell, positions), end=", ")
    #
    #     row_nb = len({cell[0] for cell in positions if cell[1] == 0})
    #     print(f"{row_nb=}")
    #     # assert step < 50 or row_nb == 1 + (step // 11) * 2
    #
    #     for test_row in [0, 1, -1, 2, -2]:
    #         cols_of_row = sorted(cell[1] for cell in positions if cell[0] == test_row)
    #         numbers_of_row = [len(positions[(test_row, col)]) for col in cols_of_row]
    #         print(f"{step=} {test_row=} {sum(numbers_of_row)}")
    #
    #         diffs[test_row].append(sum(numbers_of_row) - old_sum[test_row])
    #         old_sum[test_row] = sum(numbers_of_row)
    #
    # pprint(diffs)
    #
    # for period in range(100):
    #     if all(
    #         diffs[test_row][-period:] == diffs[test_row][-2 * period : -period]
    #         for test_row in [0, 1, -1, 2, -2]
    #     ):
    #         print("period=", period)
    #         break
    #
    # sum_on_period = [sum(diff[-period:]) for diff in diffs]
    #
    # print(sum_on_period)
    #
    # for step in range(1000):
    #     positions = move_steps(start_position, step)
    #     print(f"{step=}, {count(positions)=}")
    #
    #     row_nb = len({cell[0] for cell in positions if cell[1] == 0})
    #     print(f"{row_nb=}")
    #     # assert step < 50 or row_nb == 1 + (step // 11) * 2
    #
    #     for test_row in [0, 1, -1, 2, -2]:
    #         cols_of_row = sorted(cell[1] for cell in positions if cell[0] == test_row)
    #         numbers_of_row = [len(positions[(test_row, col)]) for col in cols_of_row]
    #
    #         if step > 100 - period:
    #             if step == 90:
    #                 print(90)
    #             i = step - (len(diffs[test_row]) - period)
    #             calculated = (
    #                 sum(diffs[test_row][: -period + 1])
    #                 + (i // period) * sum_on_period[test_row]
    #                 + sum(diffs[test_row][-period + 1 :][: i % period])
    #             )
    #         else:
    #             calculated = sum(diffs[test_row][: step + 1])
    #
    #         print(f"{sum(numbers_of_row)=} {calculated=}")
    #         assert sum(numbers_of_row) == calculated
    #         print()
    #         print()

    # positions_per_step = []
    # for step in range(600):
    #     print(step)
    #     positions = move_steps(start_position, step)
    #     positions_per_step.append({cell: len(p) for cell, p in positions.items()})
    #
    #     if step > 300 and step%10 == 0:
    #     # Sauvegarder l'objet dans le fichier avec pickle.dump
    #         with open("positions.pickle", "wb") as file:
    #             pickle.dump(positions_per_step, file)

    with open("positions450.pickle", "rb") as file:
        loaded_data = pickle.load(file)

    pprint(len(loaded_data))

    for i in range(451):
        print(i)
        positions = loaded_data[i]
        row_min = min(row for row, col in positions)
        row_max = max(row for row, col in positions)
        col_min = min(col for row, col in positions)
        col_max = max(col for row, col in positions)

        for row in range(row_min, row_max + 1):
            for col in range(col_min, col_max + 1):
                print(f"{str(positions.get((row,col), '')):^8}", end="")
            print()

    for i in range(26501365, 26501366):
        n = 1 + (i - 1) // 131

        to_copy = loaded_data[(i - 328) % 131 + 328 - 131]
        print(f"{i=} {n=} {(i - 328) % 131 + 328 -131=}")
        # expected = sum(loaded_data[i].values())
        center, second = (7450, 7421) if i % 2 == 0 else (7421, 7450)

        n_to_copy = 1 + ((i - 328) % 131 + 328 - 131 - 1) // 131

        print(f"{center=} {second=}")
        if i == 394:
            print("")
        calculated = (
            get(to_copy, -n_to_copy, 0)
            + get(to_copy, n_to_copy, 0)
            + get(to_copy, 0, n_to_copy)
            + get(to_copy, 0, -n_to_copy)
            + (n - 1)
            * (
                get(to_copy, -(n_to_copy - 1), -1)
                + get(to_copy, -(n_to_copy - 1), 1)
                + get(to_copy, (n_to_copy - 1), 1)
                + get(to_copy, (n_to_copy - 1), -1)
            )
            + get(to_copy, -(n_to_copy - 1), 0)
            + get(to_copy, (n_to_copy - 1), 0)
            + get(to_copy, 0, (n_to_copy - 1))
            + get(to_copy, 0, -(n_to_copy - 1))
            + (n - 2)
            * (
                get(to_copy, -(n_to_copy - 2), -1)
                + get(to_copy, -(n_to_copy - 2), 1)
                + get(to_copy, (n_to_copy - 2), 1)
                + get(to_copy, (n_to_copy - 2), -1)
            )
            + center * (2 * (n // 2) - 1) ** 2
            + second * (2 * ((n - 1) // 2)) ** 2
        )
        # assert expected == calculated
        return calculated


def get(positions, row, col):
    return positions.get((row, col), 0)


# 608597755415413 too low
# 608603023105276
