#!/usr/bin/env python3
'''
    A simple parser
    parses data from this format:
    100000020
    030009000
    003000800
    000000000
    000000000
    004000500
    000000000
    300000000
    * how many boards
    no empty lines are alowed
    no spaces are alowed either

    to format:
    1) either as the solver defalt input board file
    2) as lines in format:
    003020600900305001001806400008102900700000008006708200002609500800203009005010300
    200080300060070084030500209000105408000000000402706000301007040720040060004010003
    000000907000420180000705026100904000050000040000507009920108000034059000507000000
    030050040008010500460000012070502080000603000040109030250000098001020600080060020
    ...

    This is just a tmp parser
'''
import os


def write_boards_as_lines(data, file_path):
    board = ''
    line_n = 0
    formated = ''
    while line_n < len(data):
        for i in range(9):
            board += data[line_n].strip("\n")
            line_n += 1
        formated += '%s\n' % board
        board = ''
    if save_to_file(formated, file_path, None):
        print("[+] Saved to %s" % file_path)
    else:
        print("[-] Failed to save %s" % file_path)


def format_board(board):
    board = board.split("\n")
    formated = ""
    for row, row_n in zip(board, range(len(board))):
        row = row.strip("\n ")
        for number in row:
            formated += "%s " % number
        if row_n != len(board)-1:
            formated += "\n"
    return formated


def save_to_file(board, file_name, dir_path):
    if dir_path is None:
        file_path = file_name
    else:
        if dir_path[-1] == '/':
            file_path = "%s%s" % (dir_path, file_name)
        else:
            file_path = "%s/%s" % (dir_path, file_name)
    file_path = file_path.strip("\n ")
    with open(file_path, 'w') as file:
        file.write(board)
        return True
    return False


def write_boards(data, dir_path):
    board = ""
    base = "board_%d"
    board_no = 1
    line_n = 0
    while line_n < len(data):
        for i in range(9):
            board += data[line_n]
            line_n += 1
        formated = format_board(board)
        file_name = base % board_no
        board_no += 1
        if save_to_file(formated, file_name, dir_path):
            print("[+] Saved to %s" % file_name)
        else:
            print("[-] Failed to save %s" % file_name)
        board = ""


def load_file(path):
    if not os.path.isfile(path):
        raise Exception("File not found")
    if not os.access(path, os.R_OK):
        raise Exception("Can't read")
    with open(path, 'r') as file:
        data = file.readlines()
    return data


def is_dir_ok(dir_path):
    if not os.path.isdir(dir_path):
        raise Exception("No directory found")
    if not os.access(dir_path, os.W_OK):
        raise Exception("Cant write here")


def main():
    # file_path = str(input("[?] Enter file path: "))
    file_path = "unformated_boards/boards_1.txt"
    data = load_file(file_path)
    # out_path = str(input("[?] Enter output directory: "))
    out_path = "test_boards/BOARDS_AS_LINES.txt"
    # is_dir_ok(out_path)

    # write_boards(data, out_path)
    write_boards_as_lines(data, out_path)


if __name__ == '__main__':
    main()
