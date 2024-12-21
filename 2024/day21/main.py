import argparse
import sys
import os
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from lib import lib

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
TEST_FILE = os.path.join(os.path.dirname(__file__), 'test.txt')


def content() -> list[str]:
    '''Reads the input file and returns a list of strings'''
    def read_file(file: str) -> list[str]:
        if not os.path.exists(file):
            print(f"File {file} not found")
            exit(1)
        with open(file) as f:
            lines = f.readlines()
        return [line.strip() for line in lines]

    return read_file(INPUT_FILE), read_file(TEST_FILE)


def parse_data(lines: list[str]) -> any:
    '''Parses the data'''
    res = []
    for line in lines:
        res.append(line)
    return res


from itertools import permutations
def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    def dfs_paths(kpad, start, finish):
        # print(start, finish)
        _, path = lib.grid_djikstra(kpad, start, finish, '0123456789v^<>A')
        # print()
        # print(path, start, finish)
        last = path[-1][0]
        path = [p[-1] for p in path[1:]]
        valid = []
        forb = lib.grid_find(kpad, ' ')
        for perm in list(set(permutations(path))):
            p = start
            for char in perm:
                if char == 'U':
                    p = p[0] - 1, p[1]
                elif char == 'D':
                    p = p[0] + 1, p[1]
                elif char == 'R':
                    p = p[0], p[1] + 1
                elif char == 'L':
                    p = p[0], p[1] - 1
                if p == forb:
                    break
            else:
                valid.append(''.join(perm) + 'A')

        return last, list(set(valid))

    def type(kpad, start, to_type):
        # print()
        # print(to_type)
        last, pathes = dfs_paths(kpad, start, lib.grid_find(kpad, to_type))
        res = []
        for path in pathes:
            moves = ''
            for char in path:
                if char == 'U':
                    moves += '^'
                elif char == 'D':
                    moves += 'v'
                elif char == 'R':
                    moves += '>'
                elif char == 'L':
                    moves += '<'
            res.append(moves + 'A')
        return last, res

    def combs(first, seccond):
        res = []
        if first:
            for f in first:
                for s in seccond:
                    res.append(f+s)
        else:
            for s in seccond:
                res.append(s)
        return res

    data = parse_data(lines)
    n_keypad = [
        ['7', '8', '9'],
        ['4', '5', '6'],
        ['1', '2', '3'],
        [' ', '0', 'A']
    ]
    n_ptr = (3, 2)
    d_keypad = [
        [' ', '^', 'A'],
        ['<', 'v', '>']
    ]
    d_ptr = (0, 2)
    res = 0

    # for cmd in data:
    for cmd in data:
        pos = n_ptr
        moves = []
        for char in cmd:
            pos, buff = type(n_keypad, pos, char)
            moves = combs(moves, buff)

        pos = d_ptr
        rbt = []
        for move in moves:
            bufff = []
            for char in move:
                pos, buff = type(d_keypad, pos, char)
                bufff = combs(bufff, buff)
            rbt += list(set(bufff))
            # rbt += buff
        mlen = min([len(s) for s in rbt])
        rbt = [lst for lst in rbt if len(lst) == mlen]
        rbt = list(set(rbt))

        pos = d_ptr
        rbt2 = []
        for move in rbt:
            bufff = []
            # print('move= ',move)
            for char in move:
                # print(char)
                pos, buff = type(d_keypad, pos, char)
                bufff = combs(bufff, buff)
            rbt2 += list(set(bufff))
        mlen = min([len(s) for s in rbt2])
        rbt2 = list(set(rbt2))
        rbt2 = [lst for lst in rbt2 if len(lst) == mlen]
        # print(rbt2)
        num = int(re.findall(r"(\d+)", cmd)[0])
        print(f'{num} * {len(rbt2[0])}')
        res += num * len(rbt2[0])


# <<^^A>A>AvvA
# v<<AA^>AA>AvA^AvA^Av<AA^>A
# v<A<AA^>>AA<Av>A^AAvA^Av<A^>A<A>Av<A^>A<A>Av<A<A^>>AA<Av>A^A

# <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A


    return res


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    data = parse_data(lines)
    return 0


def parse_args():
    '''Parses the arguments'''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--debug",
        help="run the test samples only",
        action="store_true"
    )
    return parser.parse_args()


def main():
    '''Parses the input and solves the two problems'''
    lines, test = content()
    options = parse_args()
    print(f"Silver test: {silver(test)}")
    print(f"Gold test:   {gold(test)}")
    if options.debug:
        return
    print(f"Silver:      {silver(lines)}")
    print(f"Gold:        {gold(lines)}")


if __name__ == "__main__":
    main()
