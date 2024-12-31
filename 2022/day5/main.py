import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from lib import lib

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
TEST_FILE = os.path.join(os.path.dirname(__file__), 'test.txt')


def parse_data(content: str):
    '''Parses the data'''
    data = content.split('\n\n')
    stacks = []
    for line in lib.grid_rotate(data[0].split('\n')):
        if line[0].isdigit():
            stacks.append([char for char in line[1:] if char != ' '])
    moves = []
    for line in data[1].splitlines():
        moves.append(lib.ints(line))
    return stacks, moves


def silver(content: str, debug: bool = False):
    '''Solves the silver problem'''
    stacks, moves = parse_data(content)

    for nbr, src, dest in moves:
        for _ in range(nbr):
            stacks[dest - 1].append(stacks[src - 1].pop())

    return ''.join([st.pop() for st in stacks])


def gold(content: str, debug: bool = False):
    '''Solves the gold problem'''
    stacks, moves = parse_data(content)

    for nbr, src, dest in moves:
        buf = []
        for _ in range(nbr):
            buf.append(stacks[src - 1].pop())
        for _ in range(nbr):
            stacks[dest - 1].append(buf.pop())

    return ''.join([st.pop() for st in stacks])


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
