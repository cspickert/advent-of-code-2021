from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        return [int(line) for line in input.splitlines()]

    def part1(self, data):
        return self.analyze(data)

    def part2(self, data):
        data = [sum(data[i - 3 : i]) for i in range(3, len(data) + 1)]
        return self.analyze(data)

    def analyze(self, data):
        return sum(data[i] > data[i - 1] for i in range(1, len(data)))
