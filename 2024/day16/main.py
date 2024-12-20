import argparse
import sys
import os

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
        res.append(list(line))
    return res


def custom_cost(_, cost, path):
    if path[-1][-1] == path[-2][-1]:
        return cost + 1
    return cost + 1001


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    data = parse_data(lines)
    start = lib.grid_find(data, 'S')
    finish = lib.grid_find(data, 'E')
    return lib.grid_djikstra(lines, start, finish, '.SE', custom_cost)[0]


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    def corners(path):
        to_check = set()
        prev = path[0][-1]

        for (row, col), char in path:
            if char != prev:
                to_check.add((row, col))
            prev = char
        return to_check

    data = parse_data(lines)
    start = lib.grid_find(data, 'S')
    finish = lib.grid_find(data, 'E')

    best_cost, path = lib.grid_djikstra(data, start, finish, '.SE', custom_cost)
    pathes = [path]

    to_check = corners(path)

    seen = set()
    while to_check:
        xx, yy = to_check.pop()
        if (xx, yy) in seen:
            continue
        seen.add((xx, yy))

        data[xx][yy] = '#'

        cost, path = lib.grid_djikstra(data, start, finish, '.SE', custom_cost)
        if cost == best_cost:
            pathes.append(path)
            to_check |= corners(path)

        data[xx][yy] = '.'

    squares = set()
    for path in pathes:
        for (x, y), _ in path:
            squares.add((x, y))

    return len(squares)


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
