import argparse
import sys
import os
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from lib import lib

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
    A = int(re.findall(r'(\d+)', lines[0])[0])
    B = int(re.findall(r'(\d+)', lines[1])[0])
    C = int(re.findall(r'(\d+)', lines[2])[0])
    program = list(map(int, re.findall(r'(\d+)', lines[4])))
    return [A, B, C, program]


def calculate(A, B, C, instr) -> list[int]:
    def comboop(n):
        if n <= 3:
            return n
        elif n == 4:
            return A
        elif n == 5:
            return B
        elif n == 6:
            return C
    output = []

    i = 0
    while i < len(instr):
        opcode, operand = instr[i], instr[i + 1]
        i += 2
        if opcode == 0:
            A = A // (2 ** comboop(operand))
        elif opcode == 1:
            B = B ^ operand
        elif opcode == 2:
            B = comboop(operand) % 8
        elif opcode == 3:
            if A != 0:
                i = operand
        elif opcode == 4:
            B = B ^ C
        elif opcode == 5:
            output.append(comboop(operand) % 8)
        elif opcode == 6:
            B = A // (2 ** comboop(operand))
        elif opcode == 7:
            C = A // (2 ** comboop(operand))
    return output


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    A, B, C, instr = parse_data(lines)
    return ','.join(map(str, calculate(A, B, C, instr)))


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    _, _, _, instr = parse_data(lines)
    options = [0]
    # ans = 1
    # for i in reversed(instr):
    #     while ans % 8 != i:
    #         ans += 1
    #     ans *= 8
    # return ans // 8

    for i in range(1, len(instr) + 1):
        buffer = []
        for option in options:
            for nxt in range(8):
                test_output = calculate(option + nxt, 0, 0, instr)
                if test_output[-i:] == instr[-i:]:
                    buffer.append(option + nxt)
        options = [b * 8 for b in buffer]

    return options[0] // 8


def parse_args():
    '''Parses the arguments'''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--debug",
        help="run the test samples only",
        action="store_true"
    )
    return parser.parse_args()


def main():
    '''Parses the input and solves the two problems'''
    lines, test = content()
    options = parse_args()
    print(f"Silver test: {silver(test)}")
    print(f"Gold test:   {gold(test)}")
    if options.debug:
        return
    print(f"Silver:      {silver(lines)}")
    print(f"Gold:        {gold(lines)}")


if __name__ == "__main__":
    main()
