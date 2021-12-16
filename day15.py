import heapq

from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        return [[int(value) for value in line] for line in input.splitlines()]

    def part1(self, data):
        return self.explore(data)

    def part2(self, data):
        pass

    def explore(self, data):
        """Implementation based on:
        https://stackabuse.com/dijkstras-algorithm-in-python/"""

        risk_values = [[float("inf")] * len(row) for row in data]
        risk_values[0][0] = 0

        visited = set()
        queue = [(0, (0, 0))]

        while queue:
            _, (row, col) = heapq.heappop(queue)
            visited.add((row, col))

            for adj_row, adj_col in self.get_adjacent_coords(data, row, col):
                if (adj_row, adj_col) in visited:
                    continue

                adj_value = data[adj_row][adj_col]
                old_risk = risk_values[adj_row][adj_col]
                new_risk = risk_values[row][col] + adj_value

                if new_risk < old_risk:
                    heapq.heappush(queue, (new_risk, (adj_row, adj_col)))
                    risk_values[adj_row][adj_col] = new_risk

        last_row = len(data) - 1
        last_col = len(data[last_row]) - 1
        return risk_values[last_row][last_col]

    def get_adjacent_coords(self, data, row, col):
        for adj_row in range(row - 1, row + 2):
            if adj_row in (range(len(data))) and adj_row != row:
                yield (adj_row, col)
        for adj_col in range(col - 1, col + 2):
            if adj_col in range(len(data[row])) and adj_col != col:
                yield (row, adj_col)
