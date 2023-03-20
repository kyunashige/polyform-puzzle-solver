from polyform_puzzle_solver.grid import CubeGrid, HexGrid, Position, SquareGrid


def test_HexGrid_coord2pos():
    """
        (0, 0)  (0, 1)  (0, 2)  (0, 3)
    (1, 0)  (1, 1)  (1, 2)  (1, 3)
        (2, 1)  (2, 2)  (2, 3)  (2, 4)
    """
    for parity in [0, 1]:
        hg = HexGrid()
        hg.parity = parity
        print("----- parity =", parity, "-----")
        for loop in ["pos", "coords"]:
            print("---", loop, "---")
            for pi in range(6):
                if pi % 2 == 1 - parity:
                    print("    ", end="")
                offset = (pi + (pi + parity) % 2) // 2
                for pj in range(offset, offset + 6):
                    if loop == "pos":
                        print(f"({pi},{pj})", end="  ")
                    if loop == "coords":
                        pos = Position(pi, pj)
                        ci, cj = hg.pos2coords(pos)
                        assert pos == hg.coords2pos(ci, cj)
                        print(f"({ci},{cj})", end="  ")
                print()


if __name__ == "__main__":
    for cls in [SquareGrid, HexGrid, CubeGrid]:
        print(cls.__name__)
        g = cls()
        print("\t#dimensions:", g.dim)
        print("\t#adjacents:", len(g.adjacents))
        print("\tadjacents:", g.adjacents)

    test_HexGrid_coord2pos()
