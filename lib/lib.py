
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
DIRS_8 = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
DIRS_PATTERN_SEARCH = [(0, 1), (1, 1), (1, 0), (1, -1)]


def grid_dfs(
    data: list[str],
    pattern: str,
    direction = DIRS,
    hashing = False,
    straight = False,
) -> list[list[int]]:
    '''Finds the pattern in the grid

    Args:
        data (list[str]): the grid
        pattern (str): the sequence to find
        hashing (bool): whether to store the seen points
        straight (bool): whether the pattern has to be in a straight line
        dirs (list[tuple[int]]): the directions to move

    Returns:
        list[list[int]]: the final points
    '''
    def dfs(row: int,
        col: int,
        iter: int,
        hash: list[list[bool]],
        dirs: list[tuple[int,int]]
    ) -> list[list]:
        if not (0 <= row < len(data) and 0 <= col < len(data[0])\
            and data[row][col] == pattern[iter] and iter < len(pattern)):
            return []

        if hashing and hash[row][col]: return []
        if hashing: hash[row][col] = True

        if iter == len(pattern) - 1:
            if data[row][col] == pattern[iter]:
                return [[row, col]]
            return []

        res = []
        for rr, cc in direction:
            res += dfs(row + rr, col + cc, iter + 1, hash, dirs)
        return res

    res = []
    for row, line in enumerate(data):
        for col, char in enumerate(line):
            if char == pattern[0]:
                seen = [[False] * len(data[0]) for _ in range(len(data))]
                if straight:
                    for direct in direction:
                        res += dfs(row + direct[0], col + direct[1], 1, seen, direct)
                else:
                    res += dfs(row, col, 0, seen, direction)
    return res
