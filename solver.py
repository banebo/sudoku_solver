#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""
        Sudoku solver
"""

###########
# IMPORTS #
###########
import os
import datetime
import time
import argparse
# import random
# -- import end --

##################
# CONSOLE COLORS #
##################
W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green
Orange = '\033[33m'  # orange
B = '\033[34m'  # blue
P = '\033[35m'  # purple
C = '\033[36m'  # cyan
GR = '\033[37m'  # gray
# -- color end --


def print_board(sudoku_board):
    board = "\n"

    def get_line(l):
        line = ""
        for i in range(l):
            line += "-"
        return line
    board += G + get_line(24) + W
    board += "\n"
    # mixed up columns and rows nvm
    for row in range(9):
        board += G + "|" + W
        for column in range(9):
            node = sudoku_board[row][column]
            val = str(node['value'])
            n = " " if val == '0' else val
            # if node.is_solved():
            #     n = Orange + n + W
            board += n + (" " if (column not in [2, 5]) else G + " | " + W)
        board += G + "|\n" + W
        if row in [2, 5]:
            board += G + get_line(24) + W
            board += "\n"
    board += G + get_line(24) + W
    print(board)


def check_file_data(file_data):
    if len(file_data) != 9:
        print("[%s-%s] %sInvalid file format:%s Invalid number of rows" %
              (R, W, R, W))
        exit(1)
    for line, row in zip(file_data, range(len(file_data))):
        n = line.strip(" \n").split(" ")
        if len(n) != 9:
            e = "[%s-%s] %sInvalid file format: " \
                "%s Invalid number of columns in row %d"
            print(e % (R, W, R, W, row+1))
            exit(1)
        for i in n:
            try:
                m = int(i)
                if m < 0 or m > 9:
                    raise ValueError()
            except ValueError:
                print("[%s-%s] %sInvalid value:%s %s" %
                      (R, W, R, W, i))
                exit(1)


def init_array():
    '''
        Returns an array like [ [ false*9 ] *9 ]
        initializes the arrays for rows, columns and boxes
        each array will hold 9 lists, each with 9 boolean False values
        representing if a number exists ex. if 1 exists in the first row
        we can check that with rows_data[0][0] the same with ex. 3 in row 5:
        row_data[4][2]
    '''
    return [[False for i in range(9)] for i in range(9)]


def load_boards(file_path):
    '''
        Loads the board from a file and returns a dict 
        {'board': [[node*9]*9rows], 'rows': [[bool*9]*9rows],
         'columns': [[bool*9]*9columns], 'boxes': [[bool*9]*9boxes]}
    '''
    # initialize board and data
    board = [[] for i in range(9)]
    rows_data = init_array()
    columns_data = init_array()
    box_data = init_array()
    # check file existence & access
    if not os.path.isfile(file_path):
        print("[%s-%s] %sError:%s File does not exists on path: %s" %
              (R, W, R, W, file_path))
        exit(1)
    if not os.access(file_path, os.R_OK):
        e = "[%s-%s] %sPermission denied:%s No read permissions for file: %s"
        print(e % (R, W, R, W, file_path))
        exit(1)
    # try loading the file
    file_data = ""
    try:
        with open(file_path, 'r') as file:
            file_data = file.readlines()
    except IOError:
        print("[%s-%s] %sIOError:%s" +
              " IOError occured while reading the file: %s" %
              (R, W, R, W, file_path))
        exit(1)
    except Exception:
        print("[%s-%s] %sError:%s Error while reading the file %s" %
              (R, W, R, W, file_path))
        exit(1)
    # check if the file_data format is valid 9x9
    check_file_data(file_data)
    # load into board, rows_data, columns_data and box_data
    for line, row in zip(file_data, range(len(file_data))):
        data = line.strip(" \n").split(" ")
        for n, column in zip(data, range(9)):
            # into board
            board[row].append({'value': int(n), 'possible_vals': {}})
            node = board[row][column]
            if node['value'] != 0:
                # into rows and columns data
                rows_data[row][node['value']-1] = True
                columns_data[column][node['value']-1] = True
                # into box data
                n = 0
                # if in first three rows
                if 0 <= row and row <= 2:
                    n = 0
                # if in middle three rows
                if 3 <= row and row <= 5:
                    n = 3
                # if in last three rows
                if 6 <= row and row <= 8:
                    n = 6
                # first three columns
                if 0 <= column and column <= 2:
                    box_data[n][node['value']-1] = True  # n+0
                # middle three columns
                if 3 <= column and column <= 5:
                    box_data[n+1][node['value']-1] = True
                # last three columns
                if 6 <= column and column <= 8:
                    box_data[n+2][node['value']-1] = True

    return {'board': board, 'rows': rows_data,
            'columns': columns_data, 'boxes': box_data}


def get_args():
    parser = argparse.ArgumentParser()
    group_q_v = parser.add_mutually_exclusive_group()
    group_interactive_board_only = parser.add_mutually_exclusive_group()
    group_q_v.add_argument("-v", "--verbose",
                           dest="verbose",
                           default=False,
                           action="store_true",
                           help="Verbose")
    group_q_v.add_argument("-q", "--quiet",
                           dest="quiet",
                           default=False,
                           action="store_true",
                           help="Quiet")
    group_interactive_board_only.add_argument("-i", "--interactive",
                                              dest="interactive",
                                              action="store_true",
                                              help="Interactive mode")
    group_interactive_board_only.add_argument("-o", "--board-only",
                                              dest="board_only",
                                              action="store_true",
                                              help="Print board solution")
    parser.add_argument("-b", "--board",
                        dest="board_path",
                        required=False,
                        type=str,
                        help="Path to board file")
    return parser.parse_args()


def main():
    args = get_args()
    # TODO: set args to exec func

    # initializes the arrays for rows, columns and boxes
    # each array will hold 9 lists, each with 9 boolean False values
    # representing if a number exists ex. if 1 exists in the first row
    # we can check that with rows_data[0][0] the same with ex. 3 in row 5:
    # row_data[4][2]

    # create the nodes and the board
    # a node has a value and a set of possible values
    # the board if ofc 9x9
    if(args.board_path):
        data = load_boards(args.board_path)

    print_board(data['board'])
    print("rows[0]: ", data['rows'][0])
    print("columns[1]: ", data['columns'][1])
    print("boxes[0]: ", data['boxes'][0])




if __name__ == "__main__":
    main()
