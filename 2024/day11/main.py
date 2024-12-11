import argparse
import sys
import os
from collections import defaultdict

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
    return list(map(int, lines[0].split(' ')))


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    def grav(n: int) -> list[int]:
        if n == 0:
            return [1]
        s = str(n)
        if len(s) % 2 == 0:
            return [int(s[:len(s)//2]), int(s[len(s)//2:])]
        return [n * 2024]
    data = parse_data(lines)
    for _ in range(25):
        new = []
        for n in data:
            new += grav(n)
        data = new
    return len(data)


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    def grav(n: int) -> list[int]:
        if n == 0:
            return [1]
        s = str(n)
        if len(s) % 2 == 0:
            return [int(s[:len(s)//2]), int(s[len(s)//2:])]
        return [n * 2024]
    data = parse_data(lines)
    dd = defaultdict(int)
    for n in data:
        dd[n] += 1
    for _ in range(75):
        new = defaultdict(int)
        for k, v in dd.items():
            res = grav(k)
            for n in res:
                new[n] += v
        dd = new
    return sum(dd.values())


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
