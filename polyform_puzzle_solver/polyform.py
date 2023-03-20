from dataclasses import dataclass

import yaml

from .grid import CubeGrid, Grid, HexGrid, SquareGrid


@dataclass
class Polyform(Grid):
    shape: str
    name: str
    flip: bool = True
    grid_cls = None
    degrees_of_rotation = None

    def post_init(self):
        self.grid = self.grid_cls().from_text(self.shape)
        self.candidates = [p.to_numpy() for p in set(self.gen_candidates())]
        return self

    def area(self):
        return self.grid.area()

    def gen_candidates(self):
        basic_forms = [self.grid]
        if self.flip:
            basic_forms.append(self.grid.flip_horizontal())
        for _ in range(360 // self.degrees_of_rotation):
            yield from basic_forms
            basic_forms = [g.rotate() for g in basic_forms]


class Polyomino(Polyform, yaml.YAMLObject):
    yaml_tag = "!Polyomino"
    grid_cls = SquareGrid
    degrees_of_rotation = 90


class Polyhex(Polyform, yaml.YAMLObject):
    yaml_tag = "!Polyhex"
    grid_cls = HexGrid
    degrees_of_rotation = 60


class Polyiamond:
    yaml_tag = "!Polyiamond"
    grid_cls = None
    degrees_of_rotation = None


class Polycube:
    yaml_tag = "!Polycube"
    grid_cls = CubeGrid
    degrees_of_rotation = None
