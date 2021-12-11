from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        return [[int(c) for c in line] for line in input.splitlines()]

    def part1(self, data):
        return sum(self.step(data) for _ in range(100))

    def part2(self, data):
        total_count = len([item for row in data for item in row])
        for step_num in range(1, 1000):
            if self.step(data) == total_count:
                return step_num

    def step(self, data):
        flashes = set()
        for row in range(len(data)):
            for col in range(len(data[row])):
                data[row][col] += 1
        for row in range(len(data)):
            for col in range(len(data[row])):
                self.handle_flash(data, row, col, flashes)
        for row in range(len(data)):
            for col in range(len(data[row])):
                if data[row][col] > 9:
                    data[row][col] = 0
        return len(flashes)

    def handle_flash(self, data, row, col, flashes):
        if data[row][col] > 9 and (row, col) not in flashes:
            flashes.add((row, col))
            for adj_row, adj_col in self.get_adjacent_coords(data, row, col):
                data[adj_row][adj_col] += 1
                self.handle_flash(data, adj_row, adj_col, flashes)

    def get_adjacent_coords(self, data, row, col):
        return [
            (adj_row, adj_col)
            for adj_row in range(row - 1, row + 2)
            if adj_row in range(len(data))
            for adj_col in range(col - 1, col + 2)
            if adj_col in range(len(data[adj_row]))
            if (adj_row, adj_col) != (row, col)
        ]
