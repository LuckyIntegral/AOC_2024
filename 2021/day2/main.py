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
        el = line.split(' ')
        res.append((el[0], int(el[1])))
    return res


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    data = parse_data(lines)
    d, f = 0, 0
    for direction, value in data:
        if direction == "forward":
            f += value
        elif direction == "down":
            d += value
        else:
            d -= value
    return d * f


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    data = parse_data(lines)
    d, f, h  = 0, 0, 0
    for direction, value in data:
        if direction == "forward":
            f += value
            h += value * d
        elif direction == "down":
            d += value
        else:
            d -= value
    return h * f


def main():
    '''Parses the input and solves the two problems'''
    lines, test = content()
    if test:
        print(f"Silver test: {silver(test)}")
        input()
        print(f"Gold test:   {gold(test)}")
    print(f"Silver:      {silver(lines)}")
    print(f"Gold:        {gold(lines)}")


if __name__ == "__main__":
    main()
