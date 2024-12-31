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
    def check_number(number: int):
        n = str(number)
        for i in range(5):
            if n[i] > n[i+1]:
                return False
        for i in range(5):
            if n[i] == n[i+1]:
                return True
        return False
    data = parse_data(content)
    if debug:
        return 0
    data = lib.ints(data[0])
    counter = 0
    for i in range(data[0], data[1]):
        if check_number(i):
            counter += 1
    return counter


def gold(content: str, debug: bool = False):
    '''Solves the gold problem'''
    def check_number(number: int):
        n = str(number)
        for i in range(5):
            if n[i] > n[i+1]:
                return False
        for i in range(5):
            if n[i] == n[i+1]:
                if i == 0:
                    if n[1] != n[2]:
                        return True
                elif i == 4:
                    if n[3] != n[4]:
                        return True
                else:
                    if n[i-1] != n[i] and n[i+1] != n[i+2]:
                        return True
        return False
    data = parse_data(content)
    if debug:
        return 0
    data = lib.ints(data[0])
    counter = 0
    for i in range(data[0], data[1]):
        if check_number(i):
            counter += 1
    return counter


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
