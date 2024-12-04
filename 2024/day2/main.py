import os


INPUT_FILE = 'input.txt'
TEST_FILE = 'test.txt'

def content() -> list[str]:
    '''Reads the input file and returns a list of strings'''
    with open(INPUT_FILE) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    if not os.path.exists(TEST_FILE):
        return lines, []

    with open(TEST_FILE) as f:
        test = f.readlines()
    test = [line.strip() for line in test]

    return lines, test


def parse_data(lines: list[str]) -> any:
    '''Parses the data'''
    res = []
    for line in lines:
        res.append(list(map(int, (line.split(" ")))))
    return res


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    data = parse_data(lines)
    def is_sorted(l):
        if all(l[i] < l[i+1] for i in range(len(l)-1)):
            return True
        if all(l[i] > l[i+1] for i in range(len(l)-1)):
            return True
        return False
    def is_valid_diff(l):
        if all(1 <= abs(l[i] - l[i+1]) <= 3 for i in range(len(l)-1)):
            return True
        return False
    ans = 0
    for line in data:
        if is_sorted(line) and is_valid_diff(line):
            ans += 1
    return ans


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    data = parse_data(lines)
    def is_sorted(l):
        if all(l[i] < l[i+1] for i in range(len(l)-1)):
            return True
        if all(l[i] > l[i+1] for i in range(len(l)-1)):
            return True
        return False
    def is_valid_diff(l):
        if all(1 <= abs(l[i] - l[i+1]) <= 3 for i in range(len(l)-1)):
            return True
        return False
    ans = 0
    for line in data:
        if is_sorted(line) and is_valid_diff(line):
            ans += 1
        else:
            for i in range(len(line)):
                new = line[:i] + line[i+1:]
                if is_sorted(new) and is_valid_diff(new):
                    ans += 1
                    break
    return ans


def main():
    '''Parses the input and solves the two problems'''
    lines, test = content()
    if test:
        print(f"Silver test: {silver(test)}")
        print(f"Gold test:   {gold(test)}")
    print(f"Silver:      {silver(lines)}")
    print(f"Gold:        {gold(lines)}")


if __name__ == "__main__":
    main()
