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
    vowels = 'aeiou'
    forb = ['ab', 'cd', 'pq', 'xy']
    data = parse_data(content)
    res = 0

    for line in data:
        if any([f in line for f in forb]):
            continue
        if sum([line.count(v) for v in vowels]) < 3:
            continue
        if not any([line[i] == line[i+1] for i in range(len(line)-1)]):
            continue
        res += 1
    return res


def gold(content: str) -> int:
    '''Solves the gold problem'''
    data = parse_data(content)
    res = 0

    for line in data:
        if not any([line[i:i+2] in line[i+2:] for i in range(len(line)-1)]):
            continue
        if not any([line[i] == line[i+2] for i in range(len(line)-2)]):
            continue
        res += 1
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
