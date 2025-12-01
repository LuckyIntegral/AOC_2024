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
    curr = 50
    count = 0

    for line in data:
        d = line[0]
        c = int(line[1:])
        if d == 'L':
            curr -= c
        else:
            curr += c
        curr %= 100
        if curr == 0:
            count += 1
    return count


def gold(content: str, debug: bool = False):
    '''Solves the gold problem'''
    data = parse_data(content)
    hist = [50]

    for line in data:
        step = -1 if line[0] == 'L' else 1
        for i in range(hist[-1] + step, hist[-1] + int(line[1:]) * step + step, step):
            hist += [i]
    res = 0
    for i in hist:
        if i % 100 == 0:
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
