from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        return [int(value) for value in input.split(",")]

    def part1(self, data):
        return min(self.get_cost(data, position) for position in data)

    def part2(self, data):
        pass

    def get_cost(self, data, position):
        return sum(abs(data[i] - position) for i in range(len(data)))
