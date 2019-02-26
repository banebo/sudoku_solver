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
import random
import time
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

###################
# DATA STRUCTURES #
###################


class BadLineException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class Node:
    """
        Contains info about one square in the map
        -> __value = the value of the square
        -> __initial = the square is given at start
        -> __possible_vals = set of possible values for the square
    """
    def __init__(self, value, coords=None):
        self.__value = value
        self.__possible_vals = set()
        self.__x = None if coords is None else coords[0]
        self.__y = None if coords is None else coords[1]
        self.__solved = False if value == 0 else True

    def __str__(self):
        return str(self.__value)

    # GET
    def get_value(self): return self.__value

    def get_possible_vals(self): return self.__possible_vals

    def is_solved(self): return self.__solved

    def get_x(self): return self.__x

    def get_y(self): return self.__y

    def get_coords(self): return [self.__x, self.__y]
    # -- get end --

    # SET
    def set_solved(self, t): self.__solved = t

    def set_value(self, n): self.__value = n

    def set_possible_vals(self, poss_vals):
        self.__possible_vals = poss_vals
    # -- set end --

    def set_coords(self, x, y):
        if self.__x is None:
            self.__x = x
        if self.__y is None:
            self.__y = y

    # remove
    def remove(self, n):
        if n in self.__possible_vals:
            self.__possible_vals.remove(n)
            return True
        return False


class Board:
    """
        Class Board represents the sudoku board. The matrix of Nodes 9x9.
        The value fields which are empty is 0 (zero).
    """

    def __init__(self, file_name=None, board=None):
        if not (file_name or board):
            raise TypeError(R + "\n\n[-] Error in Board.__init__()\n" + W)
        self.__board = (self.init_board(file_name) if board is None else board)
        # check if the board is valid
        if not self.board_is_valid():
            print(R, "\n\n[-] Board values are not valid!\n", W)
            exit(1)

    def __str__(self):
        if not self.__board:
            return R + "\n[-] No board to print\n" + W
        board = "\n"

        def get_line(l):
            line = ""
            for i in range(l):
                line += "-"
            return line
        board += G + get_line(24) + W
        board += "\n"
        for y in range(9):
            board += G + "|" + W
            for x in range(9):
                if not self.__board[x][y]:
                    return R + "\n[-] Error in board at ({}, {})\n".format(x,
                                                                           y)
                node = self.__board[x][y]
                val = str(node.get_value())
                n = " " if val == '0' else val
                if node.is_solved():
                    n = Orange + n + W
                board += n + (" " if (x not in [2, 5]) else G + " | " + W)
            board += G + "|\n" + W
            if y in [2, 5]:
                board += G + get_line(24) + W
                board += "\n"
        board += G + get_line(24) + W
        return board

    def init_board(self, file_name):
        # check if the file exists
        file_name = file_name.strip()
        if os.path.isfile("boards/" + file_name):
            file_name = "boards/" + file_name
        if not (os.path.isfile(file_name)):
            print(R + "\n\n[-] Bad PATH to board file\n" + W)
            exit(1)
        file = open(file_name, "r")
        lines = file.readlines()
        file.close()
        if len(lines) != 9:
            print(R, "\n\n[-] Board format error, expected 9x9\n", W)
            exit(1)
        board = [[] for __ in range(9)]  # the board 9x9
        for line, counter in zip(lines, range(9)):
            info = line.strip(" \n").split(" ")
            if len(info) != 9:
                err = R + "\n\n[-] Invalid line {}\n" + W
                raise BadLineException(err.format(counter))
            error_msg = R + "\n\n[-] Invalid value '{}' at line {}\n" + W
            for x, val in enumerate(info):
                try:
                    n = eval(val.strip(" \n"))
                except NameError:
                    print(error_msg.format(val.strip(" \n"), counter))
                    exit(1)
                if (type(n) == int) and (0 <= n < 10):
                    board[x].append(Node(n))
                else:
                    raise BadLineException(error_msg.format(n, counter))
                    exit(1)
        # set node coords
        for y in range(9):
            for x in range(9):
                board[x][y].set_coords(x, y)
        return board

    def board_is_valid(self, board_obj=None):
        '''
            Checks if the board is valid, no double values in row, columns and
            segments. Return True / False
        '''
        board = self if board_obj is None else board_obj
        # check horizontal(l)y and vertical(l)y
        for i in range(9):
            h_line = board.get_horizontals(ypos=i)
            v_line = board.get_verticals(xpos=i)
            h_line = [i for i in h_line if i != 0]
            v_line = [i for i in v_line if i != 0]
            h_cond = len(h_line) == len(set(h_line))
            v_cond = len(v_line) == len(set(v_line))
            if not (h_cond and v_cond):
                return False
        # check segments
        for j in range(0, 9, 3):
            for i in range(0, 9, 3):
                tmp_node = Node(0, coords=[i, j])  # needed just for the coords
                segment = board.get_segment_vals(tmp_node)
                segment = [i for i in segment if i != 0]
                if len(segment) != len(set(segment)):
                    return False
        return True

    def is_solved(self, board_obj=None):
        ''' Check if the board is solved, return True / False '''
        board = self if board_obj is None else board_obj
        if len(board.get_unsolved()) == 0:
            if board.board_is_valid():
                return True
        return False

    # Get
    def get_board(self): return self.__board

    def get_unsolved(self, board_obj=None):
        ''' Return a list of nodes where value is 0 (zero) '''
        board = self.__board if board_obj is None else board_obj.get_board()
        unsolved = []
        for y in range(9):
            for x in range(9):
                if board[x][y].get_value() == 0:
                    unsolved.append(board[x][y])
        return unsolved

    def get_node(self, x, y):
        if (0 <= x < 9) and (0 <= y < 9):
            return self.__board[x][y]
        return None

    def get_verticals(self, node_obj=None, xpos=None):
        '''
            Returns a list of values in a vertical line of the board; x is same
            -> node_obj - object of type Node
            -> xpos - integer val, the x position
        '''
        if (node_obj is None) and (xpos is None):
            return []
        x = xpos if node_obj is None else node_obj.get_x()
        vals = []
        for y in range(9):
            vals.append(self.__board[x][y].get_value())
        return vals

    def get_horizontals(self, node_obj=None, ypos=None):
        '''
            Returns a list of values in a horizontal line of the board; y is
            same.
            -> node_obj - object of type Node
            -> ypos - integer val, the y postition
        '''
        if (node_obj is None) and (ypos is None):
            return []
        y = ypos if node_obj is None else node_obj.get_y()
        vals = []
        for x in range(9):
            vals.append(self.__board[x][y].get_value())
        return vals

    def get_box_vals(self, x1, x2, y1, y2):
        ''' Just a helper function for get_segment_vals() '''
        vals = []
        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                val = self.__board[x][y].get_value()
                vals.append(val)
        return vals

    def get_segment_vals(self, node_obj):
        '''
            Return a list of values in the segment where the node_obj is placed
            -> node_obj - object of type Node
        '''
        if node_obj is None:
            return []
        x_seg = [[] for __ in range(3)]
        y_seg = [[] for __ in range(3)]
        index = 0
        for i in range(9):
            x_seg[index].append(i)
            y_seg[index].append(i)
            if (i+1) % 3 == 0:
                index += 1
        x_coord, y_coord = node_obj.get_coords()
        vals = []
        for x_list in x_seg:
            if x_coord in x_list:
                for y_list in y_seg:
                    if y_coord in y_list:
                        x1, x2 = x_list[0], x_list[-1]
                        y1, y2 = y_list[0], y_list[-1]
                        vals = self.get_box_vals(x1, x2, y1, y2)
        return vals

    def assign_possible_vals(self):
        ''' Assigns possible values to all non zero value nodes '''
        if self.__board is None:
            print("\n\n[-] No board\n")
            exit(1)
        for y in range(9):
            for x in range(9):
                if self.__board[x][y].get_value() != 0:
                    continue
                node = self.__board[x][y]
                v_set = set(self.get_verticals(node_obj=node))  # vertical
                h_set = set(self.get_horizontals(node_obj=node))  # horizontal
                box_set = set(self.get_segment_vals(node_obj=node))  # segment
                if 0 in v_set:
                    v_set.remove(0)
                if 0 in h_set:
                    h_set.remove(0)
                if 0 in box_set:
                    box_set.remove(0)
                all_vals = set([i for i in range(1, 10)])
                vUhUb = set.union(v_set, h_set, box_set)  # v_set U h_set U box
                possible_vals = set.difference(all_vals, vUhUb)
                node.set_possible_vals(possible_vals)

    def solve1(self, verbose=False):
        ''' solves the board sort of recursivly using solve_rek()'''
        print("\n[*] Solving...")
        if self.solve_rek(verbose):
            print("[+] Done")
            return self
        print(R, "\n\n[-] Couldn't solve...\n", W)
        return None

    def solve_rek(self, verbose=False):
        if verbose:
            time.sleep(0.5)
            print(self.__str__())
        if self.is_solved():
            return True
        if not self.board_is_valid():
            return False
        self.assign_possible_vals()
        unsolved_list = sorted(self.get_unsolved(),
                               key=lambda x: len(x.get_possible_vals()))
        node = unsolved_list[0]
        for val in node.get_possible_vals():
            node.set_value(val)
            if self.solve_rek(verbose):
                return True
        node.set_value(0)
        return False
# -- data_struct end --

########
# MAIN #
########


def main():
    os.system("clear")
    print(P,
          '''
    _______ _     _ ______   _____  _     _ _     _
    |______ |     | |     \ |     | |____/  |     |
    ______| |_____| |_____/ |_____| |    \_ |_____|

    _______  _____         _    _ _______  ______
    |______ |     | |       \  /  |______ |_____/
    ______| |_____| |_____   \/   |______ |    \_

          ''', W)
    file = input("\n[?] Enter file name: ")
    board1 = Board(file_name=file)
    print(board1)
    now1 = datetime.datetime.now()
    solved = board1.solve1(verbose=False)
    now2 = datetime.datetime.now()
    delta_t = now2 - now1
    print("\n[*] It took me {:.2f}".format(delta_t.total_seconds()),
          "seconds to solve this.")
    print(solved, "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(R + "\n\n[-] Keyboard Interrupt\n" + W)
        exit(1)
    except EOFError:
        print(R + "\n\n[-] Exiting...\n" + W)
        exit(0)
