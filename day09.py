from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        return [[int(c) for c in line] for line in input.splitlines()]

    def part1(self, data):
        return self.calc_risk_level(data)

    def part2(self, data):
        # Find the coordinates of all low points.
        low_points = [
            (row, col)
            for row in range(len(data))
            for col in range(len(data[row]))
            if self.is_low_point(data, row, col)
        ]
        # Find all basin sizes and order from largest to smallest.
        basin_sizes = sorted(
            [self.find_basin_size(data, row, col) for row, col in low_points],
            reverse=True,
        )
        # Multiply the top 3 basin sizes.
        return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]

    def calc_risk_level(self, data):
        return sum(
            1 + data[row][col]
            for row in range(len(data))
            for col in range(len(data[row]))
            if self.is_low_point(data, row, col)
        )

    def find_basin_size(self, data, row, col, visited=None):
        if visited is None:
            visited = {(row, col)}
        else:
            visited.add((row, col))
        return 1 + sum(
            self.find_basin_size(data, adj_row, adj_col, visited)
            for adj_row, adj_col in self.get_adjacent_coords(data, row, col)
            if (adj_row, adj_col) not in visited and data[adj_row][adj_col] < 9
        )

    def is_low_point(self, data, row, col):
        return all(
            data[row][col] < value for value in self.get_adjacent_values(data, row, col)
        )

    def get_adjacent_values(self, data, row, col):
        return [
            data[adj_row][adj_col]
            for adj_row, adj_col in self.get_adjacent_coords(data, row, col)
        ]

    def get_adjacent_coords(self, data, row, col):
        coords = []
        for adj_row in range(row - 1, row + 2):
            if adj_row != row and adj_row in range(len(data)):
                coords.append((adj_row, col))
        for adj_col in range(col - 1, col + 2):
            if adj_col != col and adj_col in range(len(data[row])):
                coords.append((row, adj_col))
        return coords
