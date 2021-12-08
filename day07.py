from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        return [int(value) for value in input.split(",")]

    def part1(self, data):
        return min(
            sum(abs(value - position) for value in data)
            for position in range(min(data), max(data) + 1)
        )

    def part2(self, data):
        return min(
            sum(sum(range(1, abs(value - position) + 1)) for value in data)
            for position in range(min(data), max(data) + 1)
        )
