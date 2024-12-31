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

    for line in data:
        l, r = line.split(',')
        l, r = lib.ints(l), lib.ints(r)
        if l[0] <= r[0] and l[1] >= r[1]:
            res += 1
        elif l[0] >= r[0] and l[1] <= r[1]:
            res += 1
    return res


def gold(content: str, debug: bool = False):
    '''Solves the gold problem'''
    data = parse_data(content)
    res = 0

    for line in data:
        l, r = line.split(',')
        l, r = lib.ints(l), lib.ints(r)
        if l[0] in range(r[0], r[1] + 1) or l[1] in range(r[0], r[1] + 1):
            res += 1
        elif r[0] in range(l[0], l[1] + 1) or r[1] in range(l[0], l[1] + 1):
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
