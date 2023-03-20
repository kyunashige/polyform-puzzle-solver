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
        if isinstance(other, Position):
            return Position(*(a + b for a, b in zip(self, other)))
        if isinstance(other, int):
            return Position(*(a + other for a in self))
        raise TypeError

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

    def __getitem__(self, key):
        if key == 0:
            return self.min
        if key == 1:
            return self.max + 1
        raise IndexError


class Limits:
    def __init__(self, dim):
        self.dim = dim
        self.limits = tuple(Limit() for _ in range(self.dim))

    def __repr__(self):
        return repr(self.limits)

    def update(self, position):
        for i, pi in enumerate(position):
            self.limits[i].update(pi)

    @property
    def min(self):
        return Position(*(limit.min for limit in self.limits))

    @property
    def max(self):
        return Position(*(limit.max for limit in self.limits))


class Grid:
    dim = 2
    empty = "_"
    __heritable__ = ()

    def __init__(self):
        self.sparse = {}
        self.adjacents = tuple(self.gen_adjacents())
        self.limits = Limits(self.dim)

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

    def __getitem__(self, key, default=empty):
        return self.sparse.get(key, default)

    def __setitem__(self, key, value):
        self.limits.update(key)
        self.sparse[key] = value

    def __call__(self, fn, **kwargs):
        for attr in self.__heritable__:
            if attr not in kwargs:
                kwargs[attr] = getattr(self, attr)
        transformed = self.__class__(**kwargs)
        for position, value in self.sparse.items():
            transformed[fn(position)] = value
        assert transformed.area() == self.area()
        return transformed

    def area(self):
        return len(self.sparse)

    def size(self):
        return self.limits.max + 1

    def size_of_coords(self):
        limits = Limits(self.dim)
        for position in self.sparse.keys():
            limits.update(self.pos2coords(position))
        return limits

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

    def coords2pos(self, *coords):
        raise NotImplementedError

    def pos2coords(self, position):
        raise NotImplementedError

    def from_text(self, text):
        for ci, row in enumerate(text.splitlines()):
            for cj, char in enumerate(row):
                if char == self.empty:
                    continue
                self[self.coords2pos(ci, cj)] = char
        return self

    def to_text(self):
        array = np.full(self.size_of_coords().max + 1, " ", dtype=object)
        for position, value in self.sparse.items():
            array[tuple(self.pos2coords(position))] = value
        return np.array2string(array, separator="", formatter={"all": lambda x: str(x)})


class SquareGrid(Grid):
    def distance_fn(self, p1, p2=None):
        return abs(p1 - p2).sum()

    def normalize(self):
        mi = self.size_of_coords().min
        return self(lambda p: self.coords2pos(*(self.pos2coords(p) - mi)))

    def rotate(self):
        # degrees of rotation = 90
        return self(lambda p: Position(-p[1], p[0])).normalize()

    def flip_horizontal(self):
        # flip_vertical  = rotate^2 * flip_horizontal
        # flip_horizontaly = flip_horizontal * flip_vertical or rotate^2
        return self(lambda p: Position(p[0], -p[1])).normalize()

    def coords2pos(self, *coords):
        ci, cj = coords
        pi, pj = ci, cj
        return Position(pi, pj)

    def pos2coords(self, position):
        pi, pj = position
        ci, cj = pi, pj
        return Position(ci, cj)


class HexGrid(Grid):
    __heritable__ = ("parity",)

    def __init__(self, parity=None):
        super().__init__()
        self.parity = parity

    def distance_fn(self, p1, p2=None):
        return max(abs(p1 - p2).max(), abs((p1 - p2).diff2()))

    def normalize(self):
        mi = self.size_of_coords().min
        transformed = self.__class__(parity=(self.parity + abs(mi).sum()) % 2)
        fn = lambda p: transformed.coords2pos(*(self.pos2coords(p) - mi))
        for position, value in self.sparse.items():
            transformed[fn(position)] = value
        assert transformed.area() == self.area()
        return transformed

    def rotate(self):
        # degrees of rotation = 60
        return self(lambda p: Position(p[0] - p[1], p[0])).normalize()

    def flip_horizontal(self):
        return self(lambda p: Position(p[0], p[0] - p[1])).normalize()

    def coords2pos(self, *coords):
        ci, cj = coords
        if self.parity is None:
            self.parity = (cj + ci) % 2
        if (cj + ci) % 2 != self.parity:
            raise ValueError(f"Invalid coords: {coords}, parity={self.parity}")
        pi, pj = ci, (cj + ci) // 2
        return Position(pi, pj)

    def pos2coords(self, position):
        pi, pj = position
        ci, cj = pi, pj * 2 - pi + self.parity
        return Position(ci, cj)


class CubeGrid(Grid):
    dim = 3

    def distance_fn(self, p1, p2=None):
        return abs(p1 - p2).sum()
