# sudoku_solver v.2.1

Solves sudoku puzzles faster than v.1.1

## Content

- [Description](#description) 
- [Board file example](#board-txt-file-example) 
- [Usage](#usage)
- [Optional arguments](#optional-arguments) 
- [License](#license) 

## Description

This program is used for solving sudoku puzzles. It reads from a txt file which
contains the board. The values that are not written on the initial board are
written as 0 (zero). The numbers are separated with a space.

## Board txt file example:

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

## Usage

```bash
python3 sudoku_solver.py
```
or

```bash
chmod 777 sudoku_solver.py
```
```bash
./sudoku_solver.py 
```

## Optional arguments
Specify path to board
```bash ./solver.py -b <path_to_board>``` 
Verbose
```bash ./solver.py -v ``` 
Only output the solved board
```bash ./solver.py -s ``` 
Only output as file format
```bash ./solver.py -t ``` 


## License
[MIT](https://choosealicense.com/licenses/mit/)
