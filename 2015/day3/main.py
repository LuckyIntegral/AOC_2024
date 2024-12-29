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
            return f.read()

    return read_file(INPUT_FILE), read_file(TEST_FILE)


def parse_data(content: str) -> any:
    '''Parses the data'''
    return content.splitlines()


def silver(content: str) -> int:
    '''Solves the silver problem'''
    data = parse_data(content)
    points = set()
    cur = (0, 0)

    for char in data[0]:
        points.add(cur)
        x, y = lib.DIRS_ARROWS[char]
        cur = (cur[0] + x, cur[1] + y)
    return len(points)


def gold(content: str) -> int:
    '''Solves the gold problem'''
    data = parse_data(content)
    points = set([(0, 0)])
    cur1, cur2 = (0, 0), (0, 0)

    for idx, char in enumerate(data[0]):
        x, y = lib.DIRS_ARROWS[char]
        if idx % 2 == 0:
            cur1 = (cur1[0] + x, cur1[1] + y)
            points.add(cur1)
        else:
            cur2 = (cur2[0] + x, cur2[1] + y)
            points.add(cur2)
    return len(points)


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
