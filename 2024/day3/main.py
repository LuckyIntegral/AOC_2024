import os
import re


INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
TEST_FILE = os.path.join(os.path.dirname(__file__), 'test.txt')

def content() -> list[str]:
    '''Reads the input file and returns a list of strings'''
    def read_file(file: str) -> list[str]:
        if not os.path.exists(file):
            print(f"File {file} not found")
            exit(1)
        with open(file) as f:
            lines = f.readlines()
        return [line.strip() for line in lines]

    return read_file(INPUT_FILE), read_file(TEST_FILE)


def parse_data(lines: list[str]) -> any:
    '''Parses the data'''
    res = []
    for line in lines:
        res.append(line)
    return res


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    data = parse_data(lines)
    nums = re.findall(r'mul\((\d+),(\d+)\)', ''.join(data))
    return sum(int(a) * int(b) for a, b in nums)


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    data = parse_data(lines)
    data = re.findall(r'(mul|do|don\'t)\((\d*),?(\d*)\)', ''.join(data))
    ans = 0
    enable = True
    for r in data:
        if r[0] == 'do':
            enable = True
        elif r[0] == 'don\'t':
            enable = False
        elif enable:
            ans += int(r[1]) * int(r[2])
    return ans


def main():
    '''Parses the input and solves the two problems'''
    lines, test = content()
    print(f"Silver test: {silver(test)}")
    print(f"Gold test:   {gold(test)}")
    print(f"Silver:      {silver(lines)}")
    print(f"Gold:        {gold(lines)}")


if __name__ == "__main__":
    main()
