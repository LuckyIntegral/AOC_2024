import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from lib import lib

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
TEST_FILE = os.path.join(os.path.dirname(__file__), 'test.txt')


def parse_data(content: str):
    '''Parses the data'''
    lines = []

    for line in content.splitlines():
        a, b = line.split(' -> ')
        aa, ab = map(int, a.split(','))
        ba, bb = map(int, b.split(','))
        lines += [(aa, ab, ba, bb)]
    return lines

from collections import defaultdict

def silver(content: str, debug: bool = False):
    '''Solves the silver problem'''
    data = parse_data(content)
    res = 0
    seen = defaultdict(int)
    for line in data:
        if line[0] == line[2]:
            minv = min(line[1], line[3])
            maxv = max(line[1], line[3])
            for i in range(minv, maxv+1):
                seen[(line[0], i)] += 1
        if line[1] == line[3]:
            minv = min(line[0], line[2])
            maxv = max(line[0], line[2])
            for i in range(minv, maxv+1):
                seen[(i, line[1])] += 1

    for k, v in seen.items():
        if v > 1:
            res += 1
    return res


def gold(content: str, debug: bool = False):
    '''Solves the gold problem'''
    data = parse_data(content)
    res = 0
    seen = defaultdict(int)
    for line in data:
        if line[0] == line[2]:
            minv = min(line[1], line[3])
            maxv = max(line[1], line[3])
            for i in range(minv, maxv+1):
                seen[(i, line[0])] += 1
        elif line[1] == line[3]:
            minv = min(line[0], line[2])
            maxv = max(line[0], line[2])
            for i in range(minv, maxv+1):
                seen[(line[1], i)] += 1
        else:
            minx = min(line[0], line[2])
            maxx = max(line[0], line[2])
            starty = line[1] if line[0] < line[2] else line[3]
            endy = line[3] if line[0] < line[2] else line[1]
            stepy = 1 if starty < endy else -1

            for x, y in zip(range(minx, maxx+1), range(starty, endy+stepy, stepy)):
                seen[(y, x)] += 1

    for k, v in seen.items():
        if v > 1:
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
