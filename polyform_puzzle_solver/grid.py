from itertools import product

import numpy as np


class Position:
    def __init__(self, *coords):
        self.coords = coords

    def __repr__(self):
        return repr(self.coords)

    def __hash__(self):
        # if `hash(tuple(self))` is used, `hash((0, -1)) == hash((0, -2))` occurs
        return sum(c * 1000**i for i, c in enumerate(self.coords, start=1))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __len__(self):
        return len(self.coords)

    def __getitem__(self, key):
        return self.coords[key]

    def __abs__(self):
        return Position(*map(abs, self))

    def __add__(self, other):
        return Position(*(a + b for a, b in zip(self, other)))

    def __iadd__(self, other):
        self.coords = (self + other).coords
        return self

    def __sub__(self, other):
        return Position(*(a - b for a, b in zip(self, other)))

    def __isub__(self, other):
        self.coords = (self - other).coords
        return self

    def __lt__(self, other):
        return self.coords < other.coords

    def sum(self):
        return sum(self.coords)

    def max(self):
        return max(self.coords)

    def diff2(self):
        assert len(self.coords) == 2
        return self.coords[0] - self.coords[1]


class Limit:
    def __init__(self):
        self.min = float("inf")
        self.max = float("-inf")

    def __repr__(self):
        return f"[{self.min}, {self.max}]"

    def update(self, value):
        self.min = min(self.min, value)
        self.max = max(self.max, value)

    def __len__(self):
        return self.max - self.min + 1

    def __getitem__(self, key):
        if key == 0:
            return self.min
        if key == 1:
            return self.max + 1
        raise IndexError


class Grid:
    dim = 2
    empty = "_"

    def __init__(self):
        self.sparse = {}
        self.adjacents = tuple(self.gen_adjacents())
        self.limits = [Limit() for _ in range(self.dim)]

    def __repr__(self):
        return "%s(text=(\n%s), limits=%s)" % (
            self.__class__.__name__,
            self.to_text(),
            self.limits,
        )

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __getitem__(self, key, default=None):
        return self.sparse.get(key, default)

    def __setitem__(self, key, value):
        for i, coord in enumerate(key):
            self.limits[i].update(coord)
        self.sparse[key] = value

    def __call__(self, fn):
        transformed = self.__class__()
        for position, value in self.sparse.items():
            transformed[fn(position)] = value
        assert transformed.area() == self.area()
        return transformed

    def translate(self, add):
        return self(lambda p: Position(*(i + di for i, di in zip(p, add))))

    def normalize(self):
        return self.translate([-l.min for l in self.limits])

    def area(self):
        return len(self.sparse)

    def size(self):
        return tuple(map(len, self.limits))

    def to_numpy(self):
        state = np.zeros(self.size(), dtype=np.int8)
        for position in self.sparse.keys():
            state[tuple(position)] = 1
        return state

    def distance_fn(self, p1, p2=None):
        raise NotImplementedError

    def distance(self, p1, p2=None):
        p2 = p2 or Position(*[0] * self.dim)
        return self.distance_fn(p1, p2)

    def is_adjacent(self, p1, p2):
        return self.distance(p1, p2) == 1

    def gen_adjacents(self):
        for dis in product([-1, 0, 1], repeat=self.dim):
            dij = Position(*dis)
            if self.distance(dij) == 1:
                yield dij

    def from_text(self, text):
        raise NotImplementedError

    def to_text(self):
        raise NotImplementedError


class SquareGrid(Grid):
    def distance_fn(self, p1, p2=None):
        return abs(p1 - p2).sum()

    def rotate(self):
        return self(lambda p: Position(-p[1], p[0])).normalize()

    def flip_x(self):
        # flip_y  = rotate^2 * flip_x
        # flip_xy = flip_x * flip_y or rotate^2
        return self(lambda p: Position(p[0], -p[1])).normalize()

    def from_text(self, text):
        for i, row in enumerate(text.splitlines()):
            for j, char in enumerate(row):
                if char == self.empty:
                    continue
                self[Position(i, j)] = char
        return self

    def to_text(self):
        text = ""
        for i in range(*self.limits[0]):
            for j in range(*self.limits[1]):
                text += self.__getitem__(Position(i, j), self.empty)
            text += "\n"
        return text


class HexGrid(Grid):
    def distance_fn(self, p1, p2=None):
        return max(abs(p1 - p2).max(), abs((p1 - p2).diff2()))


class CubeGrid(Grid):
    dim = 3

    def distance_fn(self, p1, p2=None):
        return abs(p1 - p2).sum()
