from pprint import pprint

from polyform_puzzle_solver.polyform import Polyomino


def test_Polyomino_maximum_candidates():
    omino = Polyomino(shape="o_\nxy", name="has-maximum-candidates").post_init()
    assert len(omino.candidates) == 8


if __name__ == "__main__":
    num_candidates = test_Polyomino_maximum_candidates()
    print("#Polyomino.candidates =", num_candidates)

    print("Show candidates:")
    omino = Polyomino(shape="oooo\no___", name="1つ目").post_init()
    pprint(omino.candidates)
