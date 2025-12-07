import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from lib import lib

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
TEST_FILE = os.path.join(os.path.dirname(__file__), 'test.txt')


def parse_data(content: str):
    '''Parses the data'''
    return [list(line) for line in content.splitlines()]


def silver(content: str):
    '''Solves the silver problem'''
    data = parse_data(content)
    splits = 0

    for i, line in enumerate(data[:-1]):
        for j, char in enumerate(line):
            if char == "|":
                if data[i+1][j] != "^":
                    data[i+1][j] = "|"
                elif data[i+1][j] == "^":
                    data[i+1][j+1] = "|"
                    data[i+1][j-1] = "|"
                    splits += 1
            if char == "S":
                data[i+1][j] = "|"
    return splits

from functools import cache
def gold(content: str):
    '''Solves the gold problem'''
    @cache
    def dfs(row, col):
        if row >= rows:
            return 1

        if data[row][col] == '^':
            left  = dfs(row, col-1)
            right = dfs(row, col+1)
            return left + right

        return dfs(row+1, col)

    data = parse_data(content)
    rows, cols = lib.grid_size(data)

    for col in range(cols):
        if data[0][col] == 'S':
            start = (1, col)
            break

    return dfs(*start)



def main():
    '''Parses the input and solves the two problems'''
    options = lib.parse_args()

    content = lib.read_file(TEST_FILE)
    print(f"Silver test: {silver(content)}")
    print(f"Gold test:   {gold(content)}")

    if not options.debug:
        content = lib.read_file(INPUT_FILE)
        print(f"Silver:      {silver(content)}")
        print(f"Gold:        {gold(content)}")


if __name__ == "__main__":
    main()
