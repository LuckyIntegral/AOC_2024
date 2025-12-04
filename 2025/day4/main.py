import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from lib import lib

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
TEST_FILE = os.path.join(os.path.dirname(__file__), 'test.txt')


def parse_data(content: str):
    '''Parses the data'''
    return content.splitlines()


def silver(content: str, debug: bool = False):
    '''Solves the silver problem'''
    data = parse_data(content)
    res = 0

    for row, col, _ in lib.grid_iter(data):
        if data[row][col] != '@':
            continue
        nbrs = 0
        for ni, nj, _ in lib.grid_neighbors(data, row, col, lib.DIRS_8):
            if lib.grid_in(data, ni, nj):
                if data[ni][nj] == '@':
                    nbrs += 1
        if nbrs < 4:
            res += 1
    return res


def gold(content: str, debug: bool = False):
    '''Solves the gold problem'''
    data = parse_data(content)
    data = [list(row) for row in data]
    res = 0

    change = True

    while change:
        change = False
        for row, col, _ in lib.grid_iter(data):
            if data[row][col] != '@':
                continue
            nbrs = 0
            for ni, nj, _ in lib.grid_neighbors(data, row, col, lib.DIRS_8):
                if lib.grid_in(data, ni, nj):
                    if data[ni][nj] == '@':
                        nbrs += 1
            if nbrs < 4:
                data[row][col] = '.'
                change = True
                res += 1
    return res


def main():
    '''Parses the input and solves the two problems'''
    options = lib.parse_args()

    content = lib.read_file(TEST_FILE)
    print(f"Silver test: {silver(content, debug=True)}")
    print(f"Gold test:   {gold(content, debug=True)}")

    if not options.debug:
        content = lib.read_file(INPUT_FILE)
        print(f"Silver:      {silver(content)}")
        print(f"Gold:        {gold(content)}")


if __name__ == "__main__":
    main()
