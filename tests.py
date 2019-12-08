#!/usr/bin/env python3

'''
    Tests the solver algorithm
    prints the average time per board
'''

###########
# IMPORTS #
###########
import os
import datetime
import argparse
import solver
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


def check_file_data(file_data):
    '''
        Gets a list of board strings [{board}, ...]
    '''
    for board, line_n in zip(file_data, range(len(file_data))):
        if len(board.strip("\n ")) != 81:
            print("[%s-%s] %sError%s: Invalid board on line %d: %s" %
                  (R, W, R, W, line_n, board))
            exit(1)


def load_boards(file_path):
    '''
        Loads the boards from a file and returns a list of a dicts:
        {'board': [[node*9]*9rows], 'rows': [[bool*9]*9rows],
         'columns': [[bool*9]*9columns], 'boxes': [[bool*9]*9boxes],
         'unsolved': [ {'row': int, 'column': int}*number_of_not_solved_nodes]}
        node = {'value': int, 'possible_vals': set()}
    '''
    # initialize board and data
    board = [[] for i in range(9)]
    rows_data = solver.init_array()
    columns_data = solver.init_array()
    box_data = solver.init_array()
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
    # load into board, rows_data, columns_data and box_data and add to boards
    boards = []
    curr = 0
    for line in file_data:
        line = line.strip("\n")
        for row in range(9):
            for column in range(9):
                # get the value
                n = int(line[curr])
                # into board
                board[row].append({'value': n,
                                   'possible_vals': set(),
                                   'is_default': True if n != 0
                                   else False})
                # the previously appended node (dict)
                node = board[row][column]
                if node['value'] != 0:
                    val = node['value']
                    # into rows and columns data
                    rows_data[row][val-1] = True
                    columns_data[column][val-1] = True
                    # into box data
                    box_n = solver.get_box_number(row, column)
                    box_data[box_n][val-1] = True
                else:
                    unsolved_data.append({'row': row, 'column': column})
                curr += 1
        # check if the board is valid, if not -> error & exit
        if not solver.is_board_valid(board):
            print("[%s-%s] %sValueOverlap%s: "
                  "Invalid board, values overlapping, line %d" %
                  (R, W, R, W, len(boards)))
            exit(1)
        boards.append({'board': board,
                       'rows': rows_data,
                       'columns': columns_data,
                       'boxes': box_data,
                       'unsolved': unsolved_data})
        # reset all data
        board = [[] for i in range(9)]
        rows_data = solver.init_array()
        columns_data = solver.init_array()
        box_data = solver.init_array()
        unsolved_data = []
        curr = 0
    return boards


def calculate_average_time(boards, v=False):
    total = 0.0
    solved = 0.0
    for i in range(len(boards)):
        print("[%s*%s] Solving board %d of %d" % (O, W, i+1, len(boards)),
              end='\r') if v else None
        board = boards[i]
        now1 = datetime.datetime.now()
        if solver.solve(board):
            now2 = datetime.datetime.now()
            solved += 1
            delta_t = now2 - now1
            total += delta_t.total_seconds()
        else:
            print("[%s-%s] Couldn't solve this one, line %d" %
                  (R, W, i+1))
    avg_t = total / solved
    return avg_t


def parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose',
                       dest='verbose',
                       action='store_true',
                       default=False,
                       help='Verbose')
    parser.add_argument('-b', '--boards',
                        required=False,
                        type=str,
                        dest='path',
                        help='Path to board')
    return parser.parse_args()


def verbose(boards_path):
    os.system('clear') if os.name == 'posix' else os.system('cls')
    print("\n[%s*%s] Loading boards..." % (O, W))
    boards = load_boards(boards_path)
    print("[%s+%s] Done, loaded %d boards" % (G, W, len(boards)))
    now1 = datetime.datetime.now()
    avg = calculate_average_time(boards, v=True)
    now2 = datetime.datetime.now()
    print('\n[%s+%s] Done' % (G, W))
    delta_t = now2 - now1
    print("\n[%s+%s] It took me %.3f seconds to solve %d boards" %
          (G, W, delta_t.total_seconds(), len(boards)))
    print("[%s+%s] The average time per bord is %.3f\n" %
          (G, W, avg))


def main():
    args = parse_args()
    if not args.path:
        boards_path = str(input("[%s?%s] Enter path to boards: "))
    else:
        boards_path = args.path

    if args.verbose:
        verbose(boards_path)
    else:
        boards = load_boards(boards_path)
        now1 = datetime.datetime.now()
        avg = calculate_average_time(boards)
        now2 = datetime.datetime.now()
        delta_t = now2 - now1
        print("\n[%s+%s] It took me %.4f seconds to solve %d boards" %
              (G, W, delta_t.total_seconds(), len(boards)))
        print("[%s+%s] The average time per bord is %.3f\n" %
              (G, W, avg))


if __name__ == "__main__":
    main()
