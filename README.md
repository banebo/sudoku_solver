#sudoku_solver#

Solves sudoku puzzles. 

##Description

This program is used for solving sudoku puzzles. It reads from a txt file which
contains the board. The values that are not written on the initial board are
written as 0 (zero). The numbers are separated with a space.

Board txt file example:

```txt
        4 5 0 3 0 1 0 0 6
        3 0 8 6 0 0 0 9 0
        6 7 0 4 2 8 3 0 0
        8 0 1 5 6 0 0 2 0
        2 4 5 9 8 7 1 0 0
        9 6 0 2 1 3 5 0 0
        0 9 6 0 5 0 0 0 1
        1 8 3 7 4 9 6 5 2
        0 2 4 1 3 6 0 0 0
```

##Usage

```bash
python3 sudoku_solver.py <path_to_board>
```
or

```bash
chmod 777 sudoku_solver.py
```
```bash
./sudoku_solver.py <path_to_board>
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
