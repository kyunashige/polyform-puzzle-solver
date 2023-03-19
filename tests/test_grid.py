from polyform_puzzle_solver.grid import CubeGrid, HexGrid, SquareGrid

if __name__ == "__main__":
    for cls in [SquareGrid, HexGrid, CubeGrid]:
        print(cls.__name__)
        g = cls()
        print("\t#dimensions:", g.dim)
        print("\t#adjacents:", len(g.adjacents))
        print("\tadjacents:", g.adjacents)
