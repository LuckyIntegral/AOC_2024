import os
from collections import defaultdict
from functools import cmp_to_key

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
    updates = []
    conditions = []
    reached = False
    for line in lines:
        if line == '':
            reached = True
        else:
            if reached:
                conditions.append([int(n) for n in line.split(',')])
            else:
                updates.append([int(n) for n in line.split('|')])
    return updates, conditions


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    data = parse_data(lines)
    dd = defaultdict(list)
    for k, v in data[0]:
        dd[k].append(v)
    correct = []
    for nums in data[1]:
        for idx, val in enumerate(nums):
            if not all([n not in dd[val] for n in nums[:idx]]) and all([n in dd[val] for n in nums[idx+1:]]):
                break
        else:
            correct.append(nums)
    ans = 0
    for lst in correct:
        ans += lst[(len(lst)//2)]
    return ans


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    data = parse_data(lines)
    dd = defaultdict(list)
    for k, v in data[0]:
        dd[k].append(v)
    incorrect = []
    for nums in data[1]:
        for idx, val in enumerate(nums):
            if not all([n not in dd[val] for n in nums[:idx]]) and all([n in dd[val] for n in nums[idx+1:]]):
                incorrect.append(nums)
                break
    ans = 0
    for nums in incorrect:
        # order doesnt matter (ascending or descending), matters only if its sorted:)
        nums = list(sorted(nums, key=cmp_to_key(lambda a, b: -1 if b in dd[a] else 1)))
        ans += nums[(len(nums)//2)]
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
