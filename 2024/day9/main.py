import argparse
import os


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
    data = parse_data(lines)[0]
    mem = []
    for idx, char in enumerate(data):
        if idx % 2 == 0:
            mem += [idx // 2] * int(char)
        else:
            mem += [-1] * int(char)
    l, r = 0, len(mem) - 1
    while l < r:
        if mem[l] == -1:
            mem[l], mem[r] = mem[r], mem[l]
            while mem[r] == -1:
                r -= 1
        l += 1
    mem = mem[:r+1]
    ans = 0
    for idx, val in enumerate(mem):
        ans += idx * val
    return ans


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    data = parse_data(lines)[0]
    mem = {}
    smm = 0
    for idx, char in enumerate(data):
        if idx % 2 == 0:
            mem[smm] = [idx // 2] * int(char)
        else:
            mem[smm] = [-1] * int(char)
        smm += int(char)

    r = len(mem.keys()) - 1
    moved = True
    keys = list(mem.keys())
    keys.sort()

    while r > 0:
        if mem[keys[r]][0] == -1:
            r -= 1
            continue
        l = 0
        moved = False
        while l < r and not moved:
            if mem[keys[l]][0] == -1 and len(mem[keys[l]]) >= len(mem[keys[r]]):
                if len(mem[keys[l]]) > len(mem[keys[r]]):
                    mem[keys[l] + len(mem[keys[r]])] = [-1] * (len(mem[keys[l]]) - len(mem[keys[r]]))
                    keys += [keys[l] + len(mem[keys[r]])]
                mem[keys[l]] = mem[keys[r]]
                mem[keys[r]] = [-1] * len(mem[keys[r]])
                moved = True
                keys.sort()
            l += 1
        if not moved:
            r -= 1

    idx = 0
    ans = 0
    for key in list(sorted(mem.keys())):
        for val in mem[key]:
            if val != -1:
                ans += idx * val
            idx += 1

    return ans


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
