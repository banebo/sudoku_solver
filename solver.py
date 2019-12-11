#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""
        Sudoku solver
"""

# TODO: check pairs in rows and columns
# TODO: if len(pos_vals)==1 -> set it as a value; u svakoj rekurziji napravi
# listu takvih noda posle assign_poss_vals, setuj kao value svima njima, kreni
# dalje, pri izlasku iz rekurzije resetuj te node

###########
# IMPORTS #
###########
import os
import datetime
import argparse
# -- import end --

##################
# CONSOLE COLORS #
##################
W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green
O = '\033[33m'  # orange
B = '\033[34m'  # blue
P = '\033[35m'  # purple
C = '\033[36m'  # cyan
GR = '\033[37m'  # gray
# -- color end --


def remove(unsolved, index):
    del unsolved[index]
    return unsolved


def get_best_node(board, unsolved):
    '''
        Returns a dict with data about the node with the least
        amount of possible values
        {'node': node, 'row': row, 'column': column, 'unsolved_pos': int}
    '''
    if len(unsolved) <= 0:
        return None
    nodes = []
    for node in unsolved:
        row = node['row']
        column = node['column']
        nodes.append(board[row][column])
    nodes = sorted(nodes, key=lambda x: len(x['possible_vals']))
    best_node = nodes[0]
    # find coords and position in usnolved list
    i = 0
    for node, i in zip(unsolved, range(len(unsolved))):
        row = node['row']
        column = node['column']
        if board[row][column] == best_node:
            break
    return {'node': best_node, 'row': row, 'column': column, 'unsolved_pos': i}


def solve_rek(data):
    # if is solved, exit
    if is_solved(data):
        return True
    # if is populated but not solved
    if len(data['unsolved']) <= 0:
        return False
    # assign possible values for unsolved nodes
    data = assign_possible_vals(data)
    # get best node data
    node_data = get_best_node(data['board'], data['unsolved'])
    # extract data for simplicity
    node = node_data['node']
    row = node_data['row']
    column = node_data['column']
    uns_pos = node_data['unsolved_pos']
    # remove from unsolved
    data['unsolved'] = remove(data['unsolved'], uns_pos)
    for value in node['possible_vals']:
        # set the value
        node['value'] = value
        # update data
        box_n = get_box_number(row, column)
        data['rows'][row][value-1] = True
        data['columns'][column][value-1] = True
        data['boxes'][box_n][value-1] = True
        # solve further
        if solve_rek(data):
            return True
        # reset values
        node['value'] = 0
        data['rows'][row][value-1] = False
        data['columns'][column][value-1] = False
        data['boxes'][box_n][value-1] = False
    # add back to unsolved
    data['unsolved'].append({'row': row, 'column': column})
    return False


def solve(data):
    if is_solved(data):
        return True
    return solve_rek(data)


def is_solved(data):
    return is_board_valid(data['board']) and len(data['unsolved']) <= 0


def is_board_valid(board):
    '''
        Gets only the board as argument and check if it is valid
        Returns True/False
    '''
    rows = init_array()
    columns = init_array()
    boxes = init_array()
    for row in range(9):
        for column in range(9):
            node = board[row][column]
            if node['value'] == 0:
                continue
            val = node['value']
            box_n = get_box_number(row, column)
            # check if already exists, if so -> return False
            if rows[row][val-1] or \
               columns[column][val-1] or \
               boxes[box_n][val-1]:
                return False
            # set True (exists)
            rows[row][val-1] = True
            columns[column][val-1] = True
            boxes[box_n][val-1] = True
    return True


def get_col_vals(board, columns, column):
    '''
        Get the board, the column matrix and the column number
        Returns a set of values for that column which already exist (value!=0)
    '''
    vals = set()
    column_data = columns[column]
    for n in range(9):
        if column_data[n]:
            vals.add(n+1)  # add n+1 as possible value
    return vals


def get_row_vals(board, rows, row):
    '''
        Get the board, rows matrix and the row number
        Returns a set of values for that row which already exist (value != 0)
    '''
    vals = set()
    row_data = rows[row]
    for n in range(9):
        if row_data[n]:
            vals.add(n+1)  # add n+1 as poosible value
    return vals


def get_box_vals(board, boxes, row, column):
    '''
        Get the board, the boxes boolen matrix, the row number and
        the column number.
        Returns a set of values for that box whitch already exist (value != 0)
    '''
    box_n = get_box_number(row, column)  # get box number
    box = boxes[box_n]  # get box list
    # get poss values for box
    vals = set()
    for n in range(9):
        if box[n]:
            vals.add(n+1)
    return vals


def assign_possible_vals(data):
    '''
        Assigns possible values for each node
        keys in dict:
            board -> the board [[{'value': int, 'possible_vals': set()}*9]*9]
            rows -> matrix of booleans for row data [[bool*9] *9]
            columns -> matrix of boolean for columns data [[bool*9] *9]
            boxes -> matrix of booleans for columns data [[bool*9] *9]
            unsolved -> [{'row': int, 'column': int} *number_of_unsolved_nodes]
    '''
    if len(data['unsolved']) <= 0:
        return data
    # extract data
    board = data['board']
    rows = data['rows']
    boxes = data['boxes']
    columns = data['columns']
    # all values 1 <= x <= 9
    all_vals = set([i for i in range(1, 9+1)])
    for node in data['unsolved']:
        row = node['row']
        column = node['column']
        row_vals = get_row_vals(board, rows, row)
        column_vals = get_col_vals(board, columns, column)
        box_vals = get_box_vals(board, boxes, row, column)
        # check if 0 exists, if true -> remove it
        column_vals.remove(0) if 0 in column_vals else None
        row_vals.remove(0) if 0 in row_vals else None
        box_vals.remove(0) if 0 in box_vals else None
        # calculate possible values
        rUcUb = set.union(row_vals, column_vals, box_vals)
        possible_vals = set.difference(all_vals, rUcUb)
        board[row][column]['possible_vals'] = possible_vals
    return data


def str_board(sudoku_board):
    board = "\n"

    h_separator = G
    for i in range(25):
        h_separator += "-"
    h_separator += W
    v_separator = '%s%s%s' % (G, '|', W)
    board += '%s\n' % h_separator
    for row in range(9):
        board += v_separator
        for column in range(9):
            node = sudoku_board[row][column]
            val = str(node['value'])
            n = " " if val == '0' else val
            if node['is_default']:
                n = '%s%s%s' % (O, n, W)
            n = ' %s' % n if column == 0 else n
            board += '%s%s' % (n, " " if column not in [2, 5]
                               else G + " | " + W)
        board += '%s\n' % v_separator
        if row in [2, 5]:
            board += '%s\n' % h_separator
    board += h_separator
    return board


def get_box_number(row, column):
    '''
        Determens in which box the node is, return an int, 0 <= int <= 9
        0 | 1 | 2
        3 | 4 | 5
        6 | 7 | 8
    '''
    # if in first three rows (default)
    n = 0
    # if in middle three rows
    if 3 <= row and row <= 5:
        n = 3
    # if in last three rows
    elif 6 <= row and row <= 8:
        n = 6
    # first three columns
    if 0 <= column and column <= 2:
        return n
    # middle three columns
    elif 3 <= column and column <= 5:
        return n+1
    # last three columns
    elif 6 <= column and column <= 8:
        return n+2


def check_file_data(file_data):
    if len(file_data) != 9:
        print("[%s-%s] %sInvalid file format%s: Invalid number of rows" %
              (R, W, R, W))
        exit(1)
    for line, row in zip(file_data, range(len(file_data))):
        n = line.strip(" \n").split(" ")
        if len(n) != 9:
            print("[%s-%s] %sInvalid file format%s: "
                  "Invalid number of columns in row %d" %
                  (R, W, R, W, row+1))
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


def load_board(file_path):
    '''
        Loads the board from a file and returns a dict
        {'board': [[node*9]*9rows], 'rows': [[bool*9]*9rows],
         'columns': [[bool*9]*9columns], 'boxes': [[bool*9]*9boxes],
         'unsolved': [ {'row': int, 'column': int}*number_of_not_solved_nodes]}
        node = {'value': int, 'possible_vals': set()}
    '''
    # initialize board and data
    board = [[] for i in range(9)]
    rows_data = init_array()
    columns_data = init_array()
    box_data = init_array()
    unsolved_data = []
    # check file existence & access
    if not os.path.isfile(file_path):
        print("[%s-%s] %sError%s: File does not exists on path: %s" %
              (R, W, R, W, file_path))
        exit(1)
    if not os.access(file_path, os.R_OK):
        e = "[%s-%s] %sPermission denied%s: No read permissions for file: %s"
        print(e % (R, W, R, W, file_path))
        exit(1)
    # try loading the file
    try:
        with open(file_path, 'r') as file:
            file_data = file.readlines()
    except IOError:
        print("[%s-%s] %sIOError%s:"
              " IOError occured while reading the file: %s" %
              (R, W, R, W, file_path))
        exit(1)
    except Exception:
        print("[%s-%s] %sError%s: Error while reading the file %s" %
              (R, W, R, W, file_path))
        exit(1)
    # check if the file_data format is valid 9x9
    check_file_data(file_data)
    # load into board, rows_data, columns_data and box_data
    for line, row in zip(file_data, range(len(file_data))):
        line = line.strip(" \n").split(" ")
        for n, column in zip(line, range(9)):  # for each number in a row-line
            # into board
            board[row].append({'value': int(n), 'possible_vals': set(),
                               'is_default': True if int(n) != 0 else False})
            node = board[row][column]  # the previously appended node (dict)
            if node['value'] != 0:
                # into rows and columns data
                rows_data[row][node['value']-1] = True
                columns_data[column][node['value']-1] = True
                # into box data
                # if in first three rows
                box_n = get_box_number(row, column)
                val = node['value']
                box_data[box_n][val-1] = True
            else:
                unsolved_data.append({'row': row, 'column': column})
    # check if the board is valid, if not -> error & exit
    if not is_board_valid(board):
        print("[%s-%s] %sValueOverlap%s: Invalid board, values overlapping" %
              (R, W, R, W))
        exit(1)
    return {'board': board, 'rows': rows_data, 'columns': columns_data,
            'boxes': box_data, 'unsolved': unsolved_data}


def get_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose",
                       dest="verbose",
                       default=False,
                       action="store_true",
                       help="Verbose")
    group.add_argument("-t", "--txt-format",
                       dest="board_only",
                       action="store_true",
                       help="Prints board to stdout in file format")
    group.add_argument("-s", "--solution-only",
                       dest="solution_only",
                       default=False,
                       action="store_true",
                       help="Print only the solution")
    parser.add_argument("-b", "--board",
                        dest="board_path",
                        required=False,
                        type=str,
                        help="Path to board file")
    return parser.parse_args()


def solution_only(data):
    if solve(data):
        print(str_board(data['board']), '\n')
        exit(0)
    else:
        exit(1)


def output_as_txt_format(data):
    board = data['board']
    if solve(data):
        line = ""
        for row in range(9):
            for column in range(9):
                line += '%d ' % board[row][column]['value']
            line = line.strip()
            line += '\n' if row != 8 else ""
        print(line)
        exit(0)
    exit(1)


def verbose(data):
    os.system('clear') if os.name == 'posix' else os.system('clear')
    print(O,
          '''
    _______ _     _ ______   _____  _     _ _     _
    |______ |     | |     \ |     | |____/  |     |
    ______| |_____| |_____/ |_____| |    \_ |_____|
    _______  _____         _    _ _______  ______
    |______ |     | |       \  /  |______ |_____/
    ______| |_____| |_____   \/   |______ |    \_
             _    _   ______       __
            | |  | | (_____ \     /  |
            | |  | |   ____) )   |_/ |
             \ \/ /   / ____/      | |
              \  /_   |  |____  _  | |
               \/(_)  |_______|(_) |_|
          ''', W)

    print(str_board(data['board']))
    if is_solved(data):
        print("[%s*%s] The board is already solved\n" % (O, W))
        exit(1)
    print("[%s*%s] Solving..." % (O, W))
    now1 = datetime.datetime.now()
    if solve(data):
        print("[%s+%s] Done" % (G, W))
        now2 = datetime.datetime.now()
        delta_t = now2 - now1
        print(str_board(data['board']))
        print("\n[%s*%s] It took me %.3f seconds to solve this.\n" %
              (O, W, delta_t.total_seconds()))
        exit(0)
    print(R, "\n\n[%s-%s] Couldn't solve this one...\n" % (R, W))
    exit(1)


def main():
    args = get_args()
    if not args.board_path:
        file_path = str(input("[%s?%s] Enter path to board: " % (P, W)))
    else:
        file_path = args.board_path

    # initializes the arrays for rows, columns, boxes and unsolved nodes
    # each array will hold 9 lists, each with 9 boolean True/False values
    # representing if a number exists ex. if 1 exists in the first row
    # we can check that with rowss[0][0] the same with ex. 3 in row 5:
    # rows[4][2]
    # data -> dict('board', 'rows', 'columns', 'boxes', 'unsolved')
    data = load_board(file_path)

    if args.verbose:
        verbose(data)
    elif args.board_only:
        output_as_txt_format(data)
    elif args.solution_only:
        solution_only(data)
    else:
        print(str_board(data['board']))
        if is_solved(data):
            print("[%s*%s] The board is already solved\n" % (O, W))
            exit(1)
        if solve(data):
            print("[%s+%s] Solved:" % (G, W))
            print(str_board(data['board']), '\n')
        else:
            print("[%s-%s] Couldn't solve this one...\n" % (R, W))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[%s-%s] Keyboard Interrupt\n" % (R, W))
        exit(1)
    except EOFError:
        print("\n\n[%s-%s] Exiting...\n" % (R, W))
        exit(0)
