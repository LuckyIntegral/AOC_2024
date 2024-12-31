import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from lib import lib

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
TEST_FILE = os.path.join(os.path.dirname(__file__), 'test.txt')


def parse_data(content: str):
    '''Parses the data'''
    return content.splitlines()[0]

from collections import deque
def silver(content: str, debug: bool = False):
    '''Solves the silver problem'''
    data = parse_data(content)
    buf = deque(data[:3])

    for i in range(3, len(data)):
        buf.append(data[i])
        if len(set(buf)) == 4:
            return i + 1
        buf.popleft()
    return -1


def gold(content: str, debug: bool = False):
    '''Solves the gold problem'''
    data = parse_data(content)
    buf = deque(data[:13])

    for i in range(13, len(data)):
        buf.append(data[i])
        if len(set(buf)) == 14:
            return i + 1
        buf.popleft()
    return -1


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
