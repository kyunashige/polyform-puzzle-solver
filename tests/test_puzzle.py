from pprint import pprint

from polyform_puzzle_solver.polyform import Polyomino
from polyform_puzzle_solver.puzzle import *


def test_puzzle():
    for p1_flip in [True, False]:
        for p2_flip in [True, False]:
            puzzle = Puzzle(
                name="3x4-2p-1",
                shape="oooo\no_oo\noooo",
                puzzle_pieces=[
                    Polyomino(shape="oooo\no___", name="p1", flip=p1_flip),
                    Polyomino(shape="oooo\n__oo", name="p2", flip=p2_flip),
                ],
            ).post_init()
            solutions = puzzle.solve()
            assert len(solutions) == p1_flip + p2_flip


if __name__ == "__main__":
    puzzle = Puzzle(
        name="3x4-2p",
        shape="oooo\no_oo\noooo",
        puzzle_pieces=[
            Polyomino(shape="oooo\no___", name="p1", flip=True),
            Polyomino(shape="oooo\n__oo", name="p2", flip=True),
        ],
        fill_value="  ",
    ).post_init()
    pprint(puzzle)

    print("-" * 20)
    pprint(puzzle.name)
    pprint(puzzle.state)
    for piece in puzzle.puzzle_pieces:
        pprint((piece.name, len(piece.candidates)))
        pprint(piece.grid.to_numpy())

    print("-" * 20)
    if puzzle.solve():
        pprint(puzzle.visualize_all_solutions())
    else:
        print("No solution.")

    print("-" * 20)
    pprint(puzzle)
