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


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    def dfs(data, row, col, char, seen):
        if row < 0 or row >= len(data) or col < 0 or col >= len(data[0]):
            return (seen, 0)
        if data[row][col] != char or (row, col) in seen:
            return (seen, 0)
        borders = 0
        if row == 0 or data[row-1][col] != char:
            borders += 1
        if row == len(data)-1 or data[row+1][col] != char:
            borders += 1
        if col == 0 or data[row][col-1] != char:
            borders += 1
        if col == len(data[0])-1 or data[row][col+1] != char:
            borders += 1
        seen.add((row, col))
        for r, c in lib.DIRS:
            seen, bdrs = dfs(data, row+r, col+c, char, seen)
            borders += bdrs
        data[row][col] = '.'
        return seen, borders

    data = parse_data(lines)
    ans = 0

    for row, line in enumerate(data):
        for col, el in enumerate(line):
            if el != '.':
                square, perimetr = dfs(data, row, col, el, set())
                ans += len(square) * perimetr

    return ans


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    def dfs(data, row, col, char, seen):
        if row < 0 or row >= len(data) or col < 0 or col >= len(data[0]):
            return seen
        if data[row][col] != char or (row, col) in seen:
            return seen
        seen.add((row, col))
        for r, c in lib.DIRS:
            seen = dfs(data, row+r, col+c, char, seen)
        data[row][col] = '.'
        return seen

    def count_triples(seen):
        r_min = min(r for r, _ in seen)
        r_max = max(r for r, _ in seen)
        c_min = min(c for _, c in seen)
        c_max = max(c for _, c in seen)
        res = 0

        for r in range(r_min-1, r_max+1):
            for c in range(c_min-1, c_max+1):
                count = len([1 for rr, cc in ((0, 0), (0, 1), (1, 0), (1, 1)) if (r+rr, c+cc) in seen])
                if count == 1 or count == 3:
                    res += 1
                if count == 2:
                    if (((r+1,c+1) in seen) == ((r,c) in seen)) \
                        or (((r+1,c) in seen) == ((r,c+1) in seen)):
                        res += 2
        return res

    data = parse_data(lines)
    ans = 0

    for row, line in enumerate(data):
        for col, el in enumerate(line):
            if el != '.':
                seen = dfs(data, row, col, el, set())
                ans += len(seen) * count_triples(seen)

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
