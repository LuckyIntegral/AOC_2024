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
    res = []
    for line in lines:
        res.append(list(line))
    return res


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    def dfs(data, row, col, char, seen):
        if row < 0 or row >= len(data) or col < 0 or col >= len(data[0]):
            return (0, 0)
        if data[row][col] != char or (row, col) in seen:
            return (0, 0)
        pers = 0
        if row == 0 or data[row-1][col] != char:
            pers += 1
        if row == len(data)-1 or data[row+1][col] != char:
            pers += 1
        if col == 0 or data[row][col-1] != char:
            pers += 1
        if col == len(data[0])-1 or data[row][col+1] != char:
            pers += 1
        seen.add((row, col))
        s = 1
        for r, c in lib.DIRS:
            n = dfs(data, row+r, col+c, char, seen)
            s += n[0]
            pers += n[1]
        data[row][col] = '.'
        return s, pers

    data = parse_data(lines)
    ans = 0

    for row, line in enumerate(data):
        for col, el in enumerate(line):
            if el != '.':
                s, p = dfs(data, row, col, el, set())
                ans += s * p

    return ans


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    def dfs(data, row, col, char, seen):
        if row < 0 or row >= len(data) or col < 0 or col >= len(data[0]):
            return 0, seen
        if data[row][col] != char or (row, col) in seen:
            return 0, seen
        seen.add((row, col))
        s = 1
        for r, c in lib.DIRS:
            n = dfs(data, row+r, col+c, char, seen)
            s += n[0]
            seen |= n[1]
        data[row][col] = '.'
        return s, seen

    def count_triples(seen):
        r_min, r_max, c_min, c_max = float('inf'), float('-inf'), float('inf'), float('-inf')
        for r, c in seen:
            r_min = min(r_min, r)
            r_max = max(r_max, r)
            c_min = min(c_min, c)
            c_max = max(c_max, c)
        res = 0
        for r in range(r_min-1, r_max+1):
            for c in range(c_min-1, c_max+1):
                count = 0
                for rr, cc in ((0, 0), (0, 1), (1, 0), (1, 1)):
                    if (r+rr, c+cc) in seen:
                        count += 1
                if count == 1 or count == 3:
                    res += 1
                if count == 2:
                    if (((r+1,c+1) in seen) == ((r,c) in seen)) \
                        or (((r+1,c) in seen) == ((r,c+1) in seen)):
                        res += 2
        return res

    data = parse_data(lines)
    ans = 0

    for line in data:
        print("".join(line))

    for row, line in enumerate(data):
        for col, el in enumerate(line):
            if el != '.':
                s, seen = dfs(data, row, col, el, set())
                p = count_triples(seen)
                print(f"({row}, {col}) {el}: {s} * {p}")
                ans += s * p

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
