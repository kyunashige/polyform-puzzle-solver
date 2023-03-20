from argparse import ArgumentParser

import numpy as np

from polyform_puzzle_solver import solve_puzzle

np.set_printoptions(edgeitems=30, linewidth=10**5, formatter=dict(float=lambda x: "%.3g" % x))


def main(puzzle_name, **options):
    with solve_puzzle(f"puzzles/{puzzle_name}.yaml", **options) as puzzle:
        print("-" * 20)
        print(f"=== Puzzle Name: {puzzle.name} ===")
        print(puzzle.grid.to_text())
        print(f"=== Puzzle Pieces ({len(puzzle.puzzle_pieces)} pieces) ===")
        for piece in puzzle.puzzle_pieces:
            print(f"Name: {repr(piece.name)} (#candidates={len(piece.candidates)})")
            print(piece.grid.to_text())
        print("-" * 20)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "puzzle-name",
        type=str,
        help="Name of the puzzle to solve.",
    )
    parser.add_argument(
        "--leave-trace",
        "-t",
        action="store_true",
        help="If true, leave a trace of the search.",
    )
    parser.add_argument(
        "--indent",
        "-i",
        type=int,
        default=10,
        help="Number of spaces to indent the trace.",
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=-1,
        help="Limit the number of solutions to find (-1 for unlimited).",
    )

    args = vars(parser.parse_args())
    puzzle_name = args.pop("puzzle-name")
    options = args

    main(puzzle_name, **options)
