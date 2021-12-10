from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        return [
            [section.split(" ") for section in line.split(" | ")]
            for line in input.splitlines()
        ]

    def part1(self, data):
        return sum(
            len(output) in {2, 3, 4, 7} for _, outputs in data for output in outputs
        )

    def part2(self, data):
        pass
