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


def combs(first, second):
    if first:
        return [f + s for f in first for s in second]
    return list(second)


def find_first_robot(cmd):
    def find_first_stage_hardcode(pos, char):
        end = lib.grid_find(n_keypad, char)
        drow = pos[0] - end[0]
        dcol = pos[1] - end[1]
        rc = '^' * abs(drow) if drow >= 0 else 'v' * abs(drow)
        cc = '<' * abs(dcol) if dcol >= 0 else '>' * abs(dcol)
        res = []
        if not (pos[1] == 0 and end[0] == 3):
            res.append(rc + cc + 'A')
        if not (end[1] == 0 and pos[0] == 3):
            res.append(cc + rc + 'A')
        return end, res
    n_keypad = [
        ['7', '8', '9'],
        ['4', '5', '6'],
        ['1', '2', '3'],
        [' ', '0', 'A']
    ]
    pos = (3, 2)
    moves = []
    for char in cmd:
        pos, buff = find_first_stage_hardcode(pos, char)
        moves = combs(moves, buff)
    return list(set(moves))


def iteration(moves):
    pos = 'A'
    res = []
    for move in moves:
        bufff = []
        for char in move:
            pos, buff = char, shortest[pos][char]
            bufff = combs(bufff, buff)
        res += set(bufff)
    mlen = min([len(s) for s in res])
    res = [lst for lst in res if len(lst) == mlen]
    return res


shortest = {
    '^': {
        '^': ['A'],
        'A': ['>A'],
        '>': ['v>A'],
        # '>': ['>vA', 'v>A'],
        'v': ['vA'],
        '<': ['v<A'],
    },
    'A': {
        '^': ['<A'],
        'A': ['A'],
        '<': ['v<<A'],
        'v': ['<vA'],
        # 'v': ['v<A', '<vA'],
        '>': ['vA'],
    },
    '<': {
        '^': ['>^A'],
        'A': ['>>^A'],
        '<': ['A'],
        'v': ['>A'],
        '>': ['>>A'],
    },
    'v': {
        '^': ['^A'],
        'A': ['^>A'],
        # 'A': ['^>A', '>^A'],
        '<': ['<A'],
        'v': ['A'],
        '>': ['>A'],
    },
    '>': {
        '^': ['<^A'],
        # '^': ['<^A', '^<A'],
        'A': ['^A'],
        '<': ['<<A'],
        'v': ['<A'],
        '>': ['A'],
    },
}

d_keypad = [
    [' ', '^', 'A'],
    ['<', 'v', '>']
]

def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    data = parse_data(lines)
    res = 0

    for cmd in data:
        rbt = moves = find_first_robot(cmd)
        print(rbt)

        for _ in range(3):
            rbt, moves = iteration(moves), rbt

        num = int(re.findall(r"(\d+)", cmd)[0])
        res += num * len(rbt[0])

    return res


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    data = parse_data(lines)
    res = 0

    for cmd in data:
        rbt = moves = find_first_robot(cmd)

        for _ in range(26):
            print(_)
            rbt, moves = iteration(moves), rbt

        num = int(re.findall(r"(\d+)", cmd)[0])
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
