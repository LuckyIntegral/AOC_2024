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
        r, l = line[:len(line) // 2], line[len(line) // 2:]
        for ch in r:
            if ch in l:
                if ch.islower():
                    res += ord(ch) - ord('a') + 1
                else:
                    res += ord(ch) - ord('A') + 26 + 1
                break
    return res


def gold(content: str, debug: bool = False):
    '''Solves the gold problem'''
    data = parse_data(content)
    res = 0
    for i in range(0, len(data), 3):
        lines = data[i:i+3]
        ch = (set(lines[0]) & set(lines[1]) & set(lines[2])).pop()
        if ch.islower():
            res += ord(ch) - ord('a') + 1
        else:
            res += ord(ch) - ord('A') + 26 + 1

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
