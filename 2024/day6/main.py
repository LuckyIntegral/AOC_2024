import argparse
import os


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

directions = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1),
}
dirs = ['^', '>', 'v', '<']

def find_guard(data: list[str]):
    '''Finds the quard'''
    for row, line in enumerate(data):
        for col, char in enumerate(line):
            if char == '^':
                return row, col

def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''

    data = parse_data(lines)
    row, col = find_guard(data)
    d = '^'
    while True:
        data[row][col] = 'X'
        nrow, ncol = row + directions[d][0], col + directions[d][1]
        if not (0 <= nrow < len(data) and 0 <= ncol < len(data[row])):
            break

        if data[nrow][ncol] == '#':
            d = dirs[(dirs.index(d) + 1) % 4]
            continue

        row, col = nrow, ncol

    return sum([line.count('X') for line in data])


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    def is_loop(row, col, d):
        '''Checks if the loop is closed'''
        seen = set()
        while True:
            nrow, ncol = row + directions[d][0], col + directions[d][1]
            if not (0 <= nrow < len(data) and 0 <= ncol < len(data[0])):
                return False

            if data[nrow][ncol] == '#':
                d = dirs[(dirs.index(d) + 1) % 4]
                continue

            row, col = nrow, ncol
            if (row, col, d) in seen:
                return True
            seen.add((row, col, d))

    data = parse_data(lines)
    row, col = find_guard(data)
    d = '^'
    loop = 0
    while True:
        nrow, ncol = row + directions[d][0], col + directions[d][1]
        if not (0 <= nrow < len(data) and 0 <= ncol < len(data[row])):
            break

        if data[nrow][ncol] == '.':
            data[nrow][ncol] = '#'
            if is_loop(row, col, d):
                loop += 1
            data[nrow][ncol] = 'X'

        if data[nrow][ncol] == '#':
            d = dirs[(dirs.index(d) + 1) % 4]
            continue

        row, col = nrow, ncol

    return loop


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
