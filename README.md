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
tar zxvf polyform_puzzle_solver-0.2.1.tar.gz
pip install polyform_puzzle_solver-0.2.1.tar.gz

# If using poetry, simply add this repo
cd <path_to_your_code>
poetry add <path_to_polyform_puzzle_solver>
```

## Example

```shell
# Solve puzzles/Polyomino/4x8-4p-1.yaml
python solve.py Polyomino/4x8-4p-1
```

```text
--------------------
=== Puzzle Name: 4x8-4p-1 ===
[[oooooooo]
 [oooooo  ]
 [oooo    ]
 [oo      ]]
=== Puzzle Pieces (4 pieces) ===
Name: 'red   ' (#candidates=8)
[[ooo]
 [o  ]]
Name: 'pink  ' (#candidates=8)
[[ooo]
 [oo ]]
Name: 'yellow' (#candidates=8)
[[oooo]
 [o   ]]
Name: 'blue  ' (#candidates=8)
[[ooooo]
 [o    ]]
--------------------
[[blue   blue   blue   blue   blue   red    red    red   ]
 [yellow yellow yellow yellow blue   red                 ]                                               
 [pink   pink   pink   yellow                            ]                                               
 [pink   pink                                            ]]                                              
1 solutions found.                    
```

## License

[GPLv3](https://github.com/kyunashige/polyform-puzzle-solver/blob/main/LICENSE)