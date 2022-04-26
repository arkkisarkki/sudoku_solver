import random
import time
from typing import List, Set


class Sudoku:
    squares: List[int]
    last_secure_state: List[int]

    def __init__(self, initial_state: List[int] = None):
        self.squares = list()

        for i in range(9 * 9):
            self.squares.append(initial_state[i] if initial_state else i)
        # self.last_secure_state = self.squares.copy()
        self.last_secure_state = list()

        # self.print()

    def get_row(self, row: int) -> List[int]:
        retval = list()
        for i in range(9):
            retval.append(self.squares[i + row * 9])
        return retval

    def get_column(self, column: int) -> List[int]:
        retval = list()
        for i in range(9):
            retval.append(self.squares[column + i * 9])
        return retval

    def get_block(self, row, column) -> List[int]:
        retval = list()
        for j in range(3):
            for i in range(3):
                retval.append(self.squares[(row * 3 + j) * 9 + i + column * 3])
        return retval

    def print(self):
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("---" * 10)
            line = " ".join([(f"| {(element if element else ' '):2}"
                              if j % 3 == 0 and j != 0
                              else f"{(element if element else ' '):2}")
                             for j, element in
                             enumerate(self.get_row(i))])
            print(line)
        print("")
        print("---" * 20)
        print("")

    def get(self, row, column):
        return self.squares[row * 9 + column]

    def get_possibilities(self, row, column) -> Set[int]:
        if self.get(row, column):
            return {self.get(row, column)}
        else:
            retval = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            for element in self.get_row(row):
                if element and element in retval:
                    retval.remove(element)
            for element in self.get_column(column):
                if element and element in retval:
                    retval.remove(element)
            for element in self.get_block(row // 3, column // 3):
                if element and element in retval:
                    retval.remove(element)
            return retval

    def step(self) -> bool:
        changed = False
        lowest_possibilities = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        lowest_possibilities_coords = (-1, -1)
        for row in range(9):
            for column in range(9):
                if not self.get(row, column):
                    possibilities = self.get_possibilities(row, column)
                    # print(f"({row},{column}): {possibilities}")

                    if len(possibilities) == 0:
                        while len(possibilities) == 0:
                            # print(f"No possible moves for ({row},{column})")

                            # Unset a random affecting square that has not been definitely set
                            possible_resets = set()

                            current_row = {(row, i) for i in range(9)}
                            current_column = {(i, column) for i in range(9)}
                            current_block_coord = (row // 3, column // 3)
                            current_block = {(current_block_coord[0] * 3 + i, current_block_coord[1] * 3 + j) for i in
                                             range(3) for j in range(3)}

                            possible_resets = possible_resets.union(current_row)
                            possible_resets = possible_resets.union(current_column)
                            possible_resets = possible_resets.union(current_block)

                            # remove current square
                            possible_resets.remove((row, column))

                            # remove all definitely set
                            for row_ in range(9):
                                for column_ in range(9):
                                    if (self.last_secure_state[row_ * 9 + column_] or not self.get(row_, column_)) and (
                                            row_, column_) in possible_resets:
                                        possible_resets.remove((row_, column_))

                            # select random to unset
                            to_unset = list(possible_resets)[random.randrange(0, len(possible_resets))]

                            # print(f"Unsetting ({to_unset[0]},{to_unset[1]})")

                            self.squares[to_unset[0] * 9 + to_unset[1]] = 0

                            # self.print()
                            possibilities = self.get_possibilities(row, column)

                        changed = False

                    if len(possibilities) <= len(lowest_possibilities):
                        lowest_possibilities = possibilities
                        lowest_possibilities_coords = (row, column)
                    if len(possibilities) == 1:
                        changed = True
                        self.squares[row * 9 + column] = possibilities.pop()

        if not changed:
            # print("No obvious choice, have to guess")
            changed = True
            self.squares[
                lowest_possibilities_coords[0] * 9 + lowest_possibilities_coords[1]] = list(lowest_possibilities)[
                random.randrange(0, len(lowest_possibilities))]
        elif not self.last_secure_state:
            # print("Updating last secure state")
            self.last_secure_state = self.squares.copy()

        # self.print()
        return changed

    def solve(self):
        loop_counter = 0
        start = time.perf_counter()
        while self.step():
            loop_counter += 1
            if 0 not in self.squares:
                break
        end = time.perf_counter()

        print(f"{loop_counter}, {end - start} s")
        return loop_counter, end - start


if __name__ == "__main__":
    # initial_state = [0, 4, 0, 0, 0, 0, 0, 2, 0,
    #                  0, 0, 2, 3, 7, 0, 0, 0, 6,
    #                  0, 0, 0, 8, 0, 0, 0, 0, 0,
    #                  5, 0, 0, 0, 0, 0, 1, 0, 0,
    #                  0, 0, 4, 2, 6, 0, 0, 0, 3,
    #                  0, 0, 0, 0, 0, 9, 0, 0, 0,
    #                  0, 0, 0, 0, 0, 4, 0, 0, 9,
    #                  0, 0, 7, 0, 0, 8, 0, 0, 0,
    #                  0, 1, 0, 7, 9, 0, 3, 0, 0]

    initial_state = [0, 3, 0, 0, 0, 0, 0, 0, 0,
                     8, 0, 0, 9, 0, 4, 0, 0, 0,
                     9, 0, 0, 0, 0, 5, 7, 0, 2,
                     6, 0, 7, 0, 0, 3, 0, 0, 9,
                     0, 0, 0, 0, 0, 0, 1, 0, 0,
                     0, 0, 5, 1, 0, 0, 0, 3, 0,
                     0, 0, 0, 4, 0, 0, 0, 2, 0,
                     4, 0, 9, 8, 0, 2, 0, 0, 7,
                     0, 0, 3, 0, 0, 0, 0, 6, 0]

    solve_count = 0
    loop_total = 0
    time_total = 0
    min_time = 0
    max_time = 0
    min_loops = 0
    max_loops = 0

    while True:
        game = Sudoku(initial_state)
        loop_counter, time_ = game.solve()

        game.print()

        solve_count += 1
        loop_total += loop_counter
        time_total += time_

        if not min_time or time_ < min_time:
            min_time = time_
        if not max_time or time_ > max_time:
            max_time = time_
        if not min_loops or loop_counter < min_loops:
            min_loops = loop_counter
        if not max_loops or loop_counter > max_loops:
            max_loops = loop_counter

        print(
            f"LOOPS: avg {loop_total / solve_count :.5f}, min: {min_loops:5}, max: {max_loops:5}. TIME: avg {time_total / solve_count:.5f} s, min: {min_time:.5f} s, max: {max_time:.5f} s")
