# Polyform Puzzle Solver

## Installation

1. Clone this repo.

```sh
git clone https://github.com/kyunashige/polyform-puzzle-solver.git
```

2. Install with path.

```sh
# If using pip, you must build first
cd <path_to_polyform_puzzle_solver>
poetry build
cd dist
tar zxvf polyform_puzzle_solver-0.2.0.tar.gz
pip install polyform_puzzle_solver-0.2.0.tar.gz

# If using poetry, simply add this repo
cd <path_to_your_code>
poetry add <path_to_polyform_puzzle_solver>
```

## Example

```shell
# Solve puzzles/Polyomino/4x8-4p-1.yaml
python solve.py Polyomino/4x8-4p-1
```

## License

[GPLv3](https://github.com/kyunashige/polyform-puzzle-solver/blob/main/LICENSE)