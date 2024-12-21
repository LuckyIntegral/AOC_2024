import argparse
import sys
import os
import re
from functools import cache


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

def find_first_robot(cmd):
    def ff(pos, char):
        n_keypad = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            [' ', '0', 'A']
        ]
        _, path = lib.grid_djikstra(n_keypad, pos, lib.grid_find(n_keypad, char), '0123456789A', annotations=lib.DIRS_ARROWS)
        last = path[-1][0]
        path = [p[-1] for p in path[1:]]
        valid = []
        forb = lib.grid_find(n_keypad, ' ')
        pathes = [list(sorted(path))] + [list(reversed(sorted(path)))]
        for perm in pathes:
            p = pos
            for char in perm:
                dr = lib.DIRS_ARROWS[char]
                p = p[0] + dr[0], p[1] + dr[1]
                if p == forb:
                    break
            else:
                valid.append(''.join(perm) + 'A')

        return last, list(set(valid))
    pos = (3, 2)
    moves = []
    for char in cmd:
        pos, buff = ff(pos, char)
        moves = combs(moves, buff)
    return moves


def combs(first, second):
    if first:
        res = [f + s for f in first for s in second]
    else:
        res = list(second)
    mlen = min(len(s) for s in res)
    return [lst for lst in res if len(lst) == mlen]


def find_path(start, to_move):
    _, path = lib.grid_djikstra(d_keypad, start, lib.grid_find(d_keypad, to_move), 'v^<>A', annotations=lib.DIRS_ARROWS)
    last = path[-1][0]
    path = [p[-1] for p in path[1:]]
    return last, path


def iteration(moves):
    pos = (0, 2)
    res = set()
    for move in moves:
        bufff = []
        for char in move:
            pos, buff = type(pos, char)
            bufff = combs(bufff, buff)
        res |= set(bufff)
    mlen = min([len(s) for s in res])
    res = [lst for lst in res if len(lst) == mlen]
    return list(res)


def type(start, to_move):
    last, path = find_path(start, to_move)
    valid = []
    forb = lib.grid_find(d_keypad, ' ')
    pathes = [list(sorted(path))] + [list(reversed(sorted(path)))]
    for perm in pathes:
        p = start
        for char in perm:
            dr = lib.DIRS_ARROWS[char]
            p = p[0] + dr[0], p[1] + dr[1]
            if p == forb:
                break
        else:
            valid.append(''.join(perm) + 'A')

    return last, list(set(valid))

d_keypad = [
    [' ', '^', 'A'],
    ['<', 'v', '>']
]

def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    data = parse_data(lines)
    res = 0

    for cmd in data:
        moves = find_first_robot(cmd)
        rbt = moves
        for _ in range(3):
            rbt, moves = iteration(moves), rbt

        num = int(re.findall(r"(\d+)", cmd)[0])
        print(f'{num} * {len(rbt[0])}')
        res += num * len(rbt[0])

    return res


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    data = parse_data(lines)
    res = 0

    for cmd in data:
        rbt = moves = find_first_robot(cmd)
        for i in range(3):
        # for i in range(5):
            # print(f'iteration {i} has {len(rbt[0])} elements')
            rbt, moves = iteration(moves), rbt
            # print(rbt)

        # print(len(rbt))
        num = int(re.findall(r"(\d+)", cmd)[0])
        print(f'{num} * {len(rbt[0])}')
        res += num * len(rbt[0])

    return res


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
