import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from lib import lib

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
TEST_FILE = os.path.join(os.path.dirname(__file__), 'test.txt')


def parse_data(content: str):
    '''Parses the data'''
    return [line.split() for line in content.splitlines()]


def silver(content: str):
    '''Solves the silver problem'''
    data = parse_data(content)
    data = lib.grid_rotate(data)
    res = 0

    for line in data:
        if line[0] == '+':
            res += sum(int(x) for x in line[1:])
        elif line[0] == '*':
            prod = 1
            for x in line[1:]:
                prod *= int(x)
            res += prod
    return res


def gold(content: str):
    '''Solves the gold problem'''
    data = content.splitlines()
    act = ''
    sample = 0
    res = 0
    char = 0

    while char < len(data[0]):
        if all(line[char] == ' ' for line in data):
            char += 1
            continue
        if data[-1][char] in '*+':
            act = data[-1][char]
            res += sample
            sample = 0 if act == '+' else 1
        buf = ''.join(line[char] for line in data[:-1])
        sample = (sample + int(buf) if act == '+' else sample * int(buf))
        char += 1
    return res + sample


def main():
    '''Parses the input and solves the two problems'''
    options = lib.parse_args()

    content = lib.read_file(TEST_FILE)
    print(f"Silver test: {silver(content)}")
    print(f"Gold test:   {gold(content)}")

    if not options.debug:
        content = lib.read_file(INPUT_FILE)
        print(f"Silver:      {silver(content)}")
        print(f"Gold:        {gold(content)}")


if __name__ == "__main__":
    main()
