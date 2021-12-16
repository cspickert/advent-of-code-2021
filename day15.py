from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        input = """\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""
        return [[int(value) for value in line] for line in input.splitlines()]

    def part1(self, data):
        pass

    def part2(self, data):
        pass

    def get_adjacent_coords(self, data, row, col):
        for adj_row in range(row - 1, row + 2):
            if adj_row in (range(len(data))):
                yield (adj_row, col)
        for adj_col in range(col - 1, col + 2):
            if adj_col in range(len(data[row])):
                yield (row, adj_col)
