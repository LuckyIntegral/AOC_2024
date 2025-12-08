import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from lib import lib

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
TEST_FILE = os.path.join(os.path.dirname(__file__), 'test.txt')


def parse_data(content: str):
    '''Parses the data'''
    dots = []

    for line in content.splitlines():
        x, y, z = map(int, line.split(","))
        dots.append((x, y, z))
    return dots


def silver(content: str, N: int):
    '''Solves the silver problem'''
    dots = parse_data(content)

    edges = []
    for i, (x1,y1,z1) in enumerate(dots):
        for j, (x2,y2,z2) in enumerate(dots[i+1:]):
            j += i+1
            d2 = (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2
            edges.append((d2, i, j))

    edges.sort()
    edges = edges[:N]
    sets = [{i} for i in range(len(dots))]

    for _, i, j in edges:
        si, sj = None, None

        for s in sets:
            if i in s:
                si = s
            if j in s:
                sj = s

        if si != sj:
            sets.remove(si)
            sets.remove(sj)
            sets.append(si | sj)

    lens = [len(s) for s in sets]
    lens.sort()
    return lens[-1] * lens[-2] * lens[-3]


def gold(content: str):
    '''Solves the gold problem'''
    dots = parse_data(content)

    edges = []
    for i, (x1,y1,z1) in enumerate(dots):
        for j, (x2,y2,z2) in enumerate(dots[i+1:]):
            j += i+1
            d2 = (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2
            edges.append((d2, i, j))

    edges.sort()
    sets = [set([i]) for i in range(len(dots))]
    hist = []

    for _, i, j in edges:
        si, sj = None, None

        for s in sets:
            if i in s:
                si = s
            if j in s:
                sj = s

        if len(sets) == 2:
            hist.append((dots[i], dots[j]))

        if si != sj:
            sets.remove(si)
            sets.remove(sj)
            sets.append(si | sj)

    return hist[-1][0][0] * hist[-1][1][0]



def main():
    '''Parses the input and solves the two problems'''
    options = lib.parse_args()

    content = lib.read_file(TEST_FILE)
    print(f"Silver test: {silver(content, 10)}")
    print(f"Gold test:   {gold(content)}")

    if not options.debug:
        content = lib.read_file(INPUT_FILE)
        print(f"Silver:      {silver(content,1000)}")
        print(f"Gold:        {gold(content)}")


if __name__ == "__main__":
    main()
