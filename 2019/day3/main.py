import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from lib import lib

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
TEST_FILE = os.path.join(os.path.dirname(__file__), 'test.txt')


def parse_data(content: str):
    '''Parses the data'''
    return [line.split(',') for line in content.splitlines()]


def silver(content: str, debug: bool = False):
    '''Solves the silver problem'''
    def get_path(points):
        path = set()
        col, row = 0, 0

        for steps in points:
            direction = steps[0]
            steps = int(steps[1:])
            for _ in range(steps):
                next = (col + lib.DIRS_CHARS[direction][0], row + lib.DIRS_CHARS[direction][1])
                col, row = next
                path.add(next)
        return path
    data = parse_data(content)
    path1 = get_path(data[0])
    path2 = get_path(data[1])
    intersections = path1 & path2

    return min(abs(x) + abs(y) for x, y in intersections)


def gold(content: str, debug: bool = False):
    '''Solves the gold problem'''
    def get_path(points):
        path = {}
        col, row, counter = 0, 0, 0

        for steps in points:
            direction = steps[0]
            steps = int(steps[1:])
            for _ in range(steps):
                next = (col + lib.DIRS_CHARS[direction][0], row + lib.DIRS_CHARS[direction][1])
                col, row = next
                counter += 1

                path[next] = counter
        return path
    data = parse_data(content)
    path1 = get_path(data[0])
    path2 = get_path(data[1])
    intersections = path1.keys() & path2.keys()

    return min(path1[key] + path2[key] for key in intersections)


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
