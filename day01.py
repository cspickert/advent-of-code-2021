from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        return [int(line) for line in input.splitlines()]

    def part1(self, data):
        return sum(data[i] > data[i - 1] for i in range(1, len(data)))

    def part2(self, data):
        pass
