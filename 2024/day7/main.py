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
        line = line.split(":")
        line[0] = int(line[0])
        line[1] = list(map(int, line[1].strip().split(" ")))
        res.append(line)
    return res


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    def dfs(final_res, res, nums, operation):
        if not nums:
            return res == final_res
        buffer = res + nums[0] if operation == "+" else res * nums[0]
        for op in ops:
            if dfs(final_res, buffer, nums[1:], op):
                return True
        return False

    data = parse_data(lines)
    ops = ['+', '*']
    ans = 0

    for res, nums in data:
        if any(dfs(res, nums[0], nums[1:], op) for op in ops):
            ans += res
    return ans


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    def dfs(final_res, res, nums, operation):
        if not nums:
            return res == final_res
        buffer = res + nums[0] if operation == "+" else res * nums[0] if operation == "*" else int(str(res) + str(nums[0]))
        for op in ops:
            if dfs(final_res, buffer, nums[1:], op):
                return True
        return False

    data = parse_data(lines)
    ops = ['+', '*', '|']
    ans = 0

    for res, nums in data:
        if any(dfs(res, nums[0], nums[1:], op) for op in ops):
            ans += res
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
