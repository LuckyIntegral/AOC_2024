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
        mx = 0
        for i, a in enumerate(line[:-1]):
            for b in line[i+1:]:
                mx = max(mx, int(a+b))
        res += mx
    return res


def gold(content: str, debug: bool = False):
    '''Solves the gold problem'''
    data = parse_data(content)
    res = 0
    for line in data:
        st = []
        for n in line[::-1]:
            n = int(n)
            if len(st) < 12:
                st.append(n)
                continue
            for i in range(11, -1, -1):
                if n >= st[i]:
                    st[i], n = n, st[i]
                else:
                    break
        res += sum(10 ** (12-i-1) * n for i, n in enumerate(st[::-1]))

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
