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
        res.append(int(line))
    return res

from functools import cache
@cache
def next_number(nbr: int) -> int:
    '''Returns the next number in the sequence'''
    def mixnprune(nbr: int, sn: int) -> int:
        return (nbr ^ sn) % 16777216

    nbr = mixnprune(nbr, nbr * 64)
    nbr = mixnprune(nbr, nbr // 32)
    nbr = mixnprune(nbr, nbr * 2048)
    return nbr


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    data = parse_data(lines)
    res = 0
    for nbr in data:
        for _ in range(2000):
            nbr = next_number(nbr)
        res += nbr
    return res

from collections import deque
from itertools import product
def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    data = parse_data(lines)
    sales = []

    for nbr in data:
        sale = []
        for _ in range(2000):
            nxt = next_number(nbr)
            sale.append([nxt % 10, nxt % 10 - nbr % 10])
            nbr = nxt
        sales.append(sale)

    subs = []
    for sale in sales:
        sub = {}
        dq = deque([0] + sale[:3])
        for i in range(3, len(sale)):
            dq.popleft()
            dq.append(sale[i])
            key = (dq[0][1], dq[1][1], dq[2][1], dq[3][1])
            if key not in sub:
                sub[key] = dq[3][0]
        subs.append(sub)

    res = 0
    for a, b, c, d in product(range(-10, 10), repeat=4):
        key = (a, b, c, d)
        buf = 0
        for sub in subs:
            if key in sub:
                buf += sub[key]
        res = max(res, buf)
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
