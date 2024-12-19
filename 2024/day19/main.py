import argparse
import sys
import os
from collections import defaultdict
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
    patterns = lines[0].split(', ')
    for line in lines[2:]:
        res.append(line)
    return (patterns, res)


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    @cache
    def dfs(curr) -> bool:
        if curr == '':
            return True
        for pattern in lookup[curr[0]]:
            if curr.startswith(pattern):
                if dfs(curr[len(pattern):]):
                    return True
        return False

    data = parse_data(lines)
    lookup = defaultdict(list)

    for pattern in data[0]:
        lookup[pattern[0]].append(pattern)

    ans = 0
    for line in data[1]:
        if dfs(line):
            ans += 1

    return ans


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    @cache
    def dfs(curr) -> int:
        if curr == '':
            return 1
        res = 0
        for pattern in lookup[curr[0]]:
            if curr.startswith(pattern):
                res += dfs(curr[len(pattern):])
        return res

    data = parse_data(lines)
    lookup = defaultdict(list)

    for pattern in data[0]:
        lookup[pattern[0]].append(pattern)

    ans = 0
    for line in data[1]:
        ans += dfs(line)

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
    print(f"Silver test: {silver(test)}")
    print(f"Gold test:   {gold(test)}")
    if options.debug:
        return
    print(f"Silver:      {silver(lines)}")
    print(f"Gold:        {gold(lines)}")


if __name__ == "__main__":
    main()
