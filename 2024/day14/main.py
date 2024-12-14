import argparse
import sys
import os
import re
from functools import reduce

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
        res.append(list(map(int, re.findall(r'(-?\d+)', line))))
    return res


def silver(lines: list[str], size) -> int:
    '''Solves the silver problem'''
    data = parse_data(lines)
    found = False
    for r in data:
        r[0] = (r[0] + 100 * r[2]) % size[0]
        r[1] = (r[1] + 100 * r[3]) % size[1]


    squares = [0,0,0,0]
    for r in data:
        if r[0] < size[0] // 2:
            if r[1] < size[1] // 2:
                squares[0] += 1
            elif r[1] >= size[1] // 2 + 1:
                squares[1] += 1
        elif r[0] >= size[0] // 2 + 1:
            if r[1] < size[1] // 2:
                squares[2] += 1
            elif r[1] >= size[1] // 2 + 1:
                squares[3] += 1
    return reduce(lambda x, y: x * y, squares)


def gold(lines: list[str], size) -> int:
    '''Solves the gold problem'''
    data = parse_data(lines)
    found = False
    ans = 0
    for i in range(1, 10000):
        for r in data:
            r[0] = (r[0] + r[2]) % size[0]
            r[1] = (r[1] + r[3]) % size[1]

        d = [['.'] * size[0] for _ in range(size[1])]
        for r in data:
            d[r[1]][r[0]] = '#'
        for row in d:
            if ''.join(row).find('#########') != -1:
                found = True
                break
        if found:
            ans = i
            break
    # for line in d:
    #     print(''.join(line))
    return ans


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

    size = (11, 7)
    print(f"Silver test: {silver(test, size)}")
    print(f"Gold test:   {gold(test, size)}")
    if options.debug:
        return
    size = (101, 103)
    print(f"Silver:      {silver(lines, size)}")
    print(f"Gold:        {gold(lines, size)}")


if __name__ == "__main__":
    main()
