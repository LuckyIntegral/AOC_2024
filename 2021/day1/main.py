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
    return list(map(int, lines))


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    data = parse_data(lines)
    prev = data[0]
    ans = 0
    for n in data:
        if n > prev:
            ans += 1
        prev = n
    return ans


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    data = parse_data(lines)
    new = []
    for i in range(len(data) - 2):
        new.append(sum(data[i:i+3]))
    return silver(new)


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
