from pprint import pprint

import polyform_puzzle_solver as solver

if __name__ == "__main__":
    puzzle = solver.load_puzzle("./puzzles/3x4-2p.yaml")
    pprint(puzzle.__dict__)
