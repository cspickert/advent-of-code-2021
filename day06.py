from functools import cache

from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        return [int(value) for value in input.split(",")]

    def part1(self, data):
        return self.simulate(data, 80)

    def part2(self, data):
        return self.simulate(data, 256)

    def simulate(self, data, days):
        return len(data) + sum(self.simulate_helper(value, days) for value in data)

    @cache
    def simulate_helper(self, value, days):
        if days == 0:
            return 0
        if value == 0:
            return (
                1
                + self.simulate_helper(6, days - 1)
                + self.simulate_helper(8, days - 1)
            )
        return self.simulate_helper(value - 1, days - 1)
