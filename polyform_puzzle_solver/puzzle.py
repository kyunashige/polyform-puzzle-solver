from contextlib import contextmanager
from dataclasses import dataclass
from pprint import pprint
from typing import Any

import numpy as np
import yaml
from tqdm import tqdm

from .grid import Position
from .polyform import Polyform


class StopRecursion(Exception):
    pass


@dataclass
class Puzzle(yaml.YAMLObject):
    yaml_tag = "!Puzzle"

    shape: str
    puzzle_pieces: list[Polyform]
    name: str = "Puzzle"
    description: str = ""
    fill_value: Any = " "

    def post_init(self):
        assert len(self.puzzle_pieces) == len(set(piece.name for piece in self.puzzle_pieces))
        for piece in self.puzzle_pieces:
            piece.post_init()

        self.grid_cls = self.puzzle_pieces[0].grid_cls
        assert all(piece.grid_cls == self.grid_cls for piece in self.puzzle_pieces)
        self.grid = self.grid_cls().from_text(self.shape)

        self.state = self.grid.to_numpy()
        self.solutions = []
        self.pbar = None
        self.set_params()
        return self

    def set_params(self, *, leave_trace=False, indent=10, limit=-1):
        self.leave_trace = leave_trace
        assert indent >= 0
        self.indent = indent
        assert limit >= -1
        self.limit = limit

    def can_place(self, ranges, piece):
        for h, rng in zip(self.state.shape, ranges):
            if h < rng.stop:
                return False
        if np.any(self.state[ranges] - piece < 0):
            return False
        return True

    def set_piece(self, ranges, piece):
        self.state[ranges] -= piece

    def update(self, solution, pid):
        self.solutions.append(solution.copy())
        self.pbar.update()
        if self.limit != -1 and len(self.solutions) == self.limit:
            raise StopRecursion(pid)

    def __set_prefix(self, count, level):
        unit = " " * self.indent
        base = unit * (2 * count + level)
        edge = "-" * (self.indent - 1) + "+" * bool(self.indent)
        info = f"[{count + 1}-{level + 1}] "
        self.prefix = {
            "StartIteration": base + "+" + edge + info,
            "is_header=True": base + "|" + " • ",
            "is_header=False": base + "|" + "   ",
            "Count & Level": info,
        }

    def __tqdm_wrapper(self, seq, desc):
        if self.leave_trace:
            prefix = self.prefix["StartIteration"]
            print(prefix + desc, sep="")
            return seq
        else:
            prefix = self.prefix["Count & Level"]
            desc = desc.ljust(self.indent)[: self.indent]
            return tqdm(tuple(seq), desc=prefix + desc, leave=False)

    def __print_wrapper(self, *args, is_header=False, sep="", **kwargs):
        if self.leave_trace:
            prefix = self.prefix[f"is_header={is_header}"]
            print(prefix, *args, sep=sep, **kwargs)

    def solve_recursive(self, pid, solution):
        if self.state.sum() == 0:
            return True

        if pid == len(self.puzzle_pieces):
            return False

        piece = self.puzzle_pieces[pid]
        if self.state.sum() < piece.area():
            return False

        count = len(solution)
        self.__set_prefix(count, 0)
        self.__print_wrapper(
            f"pid = {pid}: '{piece.name}' (#candidates = {len(piece.candidates)})",
            is_header=True,
        )

        for cid, candidate in self.__tqdm_wrapper(
            enumerate(piece.candidates), desc="Candidates"
        ):
            self.__set_prefix(count, 1)
            self.__print_wrapper(f"cid = {cid}\n", candidate, is_header=True)
            condition = self.state == 1
            if candidate[0, 0] == 0:
                condition += self.state == 0
            positions = tuple(Position(*p) for p in zip(*condition.nonzero()))
            self.__print_wrapper("positions: ", positions)

            for position in self.__tqdm_wrapper(positions, desc="Positions"):
                self.__set_prefix(count, 2)
                self.__print_wrapper("position: ", position, is_header=True)
                solution.append((pid, cid, position))
                ranges = tuple(slice(i, i + k) for i, k in zip(position, candidate.shape))
                if self.can_place(ranges, candidate):
                    try:
                        self.__print_wrapper("state:\n", self.state)
                        self.set_piece(ranges, candidate)
                        self.__print_wrapper("↓ \n", self.state)
                        if self.solve_recursive(pid + 1, solution):
                            self.update(solution, pid)
                    except StopRecursion as e:
                        raise StopRecursion(pid) from e
                    finally:
                        self.set_piece(ranges, -candidate)
                solution.pop()

        if sum(piece.area() for piece in self.puzzle_pieces[pid + 1 :]) >= self.state.sum():
            try:
                if self.solve_recursive(pid + 1, solution):
                    self.update(solution, pid)
            except StopRecursion as e:
                raise StopRecursion(pid) from e

        return False

    def solve(self, *, leave_trace=False, indent=10, limit=-1):
        if self.solutions:
            return self.solutions
        self.set_params(leave_trace=leave_trace, indent=indent, limit=limit)
        with tqdm(desc="solutions found", leave=False) as self.pbar:
            if self.leave_trace:
                print()
            try:
                self.solve_recursive(pid=0, solution=[])
            except StopRecursion:
                pass
        return self.solutions

    def visualize_solution(self, sid=0):
        array = np.full(self.grid.size_of_coords().max + 1, self.fill_value, dtype=object)
        for pid, cid, offset in self.solutions[sid]:
            piece = self.puzzle_pieces[pid]
            candidate = piece.candidates[cid]
            pos_list = ((Position(*p) + offset) for p in zip(*candidate.nonzero()))
            coords_list = zip(*map(self.grid.pos2coords, pos_list))
            array[tuple(coords_list)] = piece.name
        return np.array2string(array, separator=" ", formatter={"all": lambda x: str(x)})

    def visualize_all_solutions(self):
        return {i: self.visualize_solution(i) for i, _ in enumerate(self.solutions)}


def load_puzzle(filepath):
    with open(filepath) as f:
        puzzle = yaml.load(f, Loader=yaml.FullLoader)
    return puzzle.post_init()


@contextmanager
def solve_puzzle(filepath, **kwargs):
    puzzle = load_puzzle(filepath)
    try:
        yield puzzle
        puzzle.solve(**kwargs)
    except KeyboardInterrupt:
        pass
    finally:
        num = len(puzzle.solutions)
        for visualized_solution in map(puzzle.visualize_solution, range(num)):
            print(visualized_solution)
        print(num, "solutions found.")
