from dataclasses import dataclass

import yaml

from .grid import CubeGrid, Grid, HexGrid, SquareGrid


@dataclass
class Polyform(Grid):
    shape: str
    name: str
    flip: bool = True
    grid_cls = None

    def post_init(self):
        self.grid = self.grid_cls().from_text(self.shape)
        self.candidates = [p.to_numpy() for p in set(self.gen_candidates())]
        return self

    def area(self):
        return self.grid.area()

    def gen_candidates(self):
        raise NotImplementedError


class Polyomino(Polyform, yaml.YAMLObject):
    yaml_tag = "!Polyomino"
    grid_cls = SquareGrid

    def gen_candidates(self):
        basic_forms = [self.grid]
        if self.flip:
            basic_forms.append(self.grid.flip_x())
        for _ in range(4):
            yield from basic_forms
            basic_forms = [g.rotate() for g in basic_forms]


class Polyhex(Polyform, yaml.YAMLObject):
    yaml_tag = "!Polyhex"
    grid_cls = HexGrid


class Polyiamond:
    yaml_tag = "!Polyiamond"
    grid_cls = None


class Polycube:
    yaml_tag = "!Polycube"
    grid_cls = CubeGrid
