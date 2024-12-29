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
    level = 0
    for char in data[0]:
        if char == '(':
            level += 1
        else:
            level -= 1
    return level


def gold(content: str) -> int:
    '''Solves the gold problem'''
    data = parse_data(content)
    level = 0
    for idx, char in enumerate(data[0]):
        if char == '(':
            level += 1
        else:
            level -= 1
        if level == -1:
            return idx + 1
    return -1


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
