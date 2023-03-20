from pprint import pprint

from polyform_puzzle_solver.polyform import Polyhex, Polyomino


def test_Polyomino_maximum_candidates():
    omino = Polyomino(shape="o_\nxy", name="has-maximum-candidates").post_init()
    assert len(omino.candidates) == 8
    return len(omino.candidates)


def test_Polyhex_maximum_candidates():
    omino = Polyhex(shape="o\n\nx_y", name="has-maximum-candidates").post_init()
    assert len(omino.candidates) == 12
    return len(omino.candidates)


if __name__ == "__main__":
    num_candidates = test_Polyomino_maximum_candidates()
    print("#Polyomino.candidates =", num_candidates)

    print("Show candidates:")
    omino = Polyomino(shape="oooo\no___", name="3x4-2p-1 > 1").post_init()
    pprint(omino.candidates)

    num_candidates = test_Polyhex_maximum_candidates()
    print("#Polyhex.candidates =", num_candidates)

    print("Show candidates:")
    omino = Polyhex(shape="__o_o\n_o\no", name="4x8-3p-1 > 2").post_init()
    pprint(omino.candidates)
