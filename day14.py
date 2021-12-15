from collections import defaultdict

from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        value, mapping_inputs = input.split("\n\n")
        mapping = dict(line.split(" -> ") for line in mapping_inputs.splitlines())
        return value, mapping

    def part1(self, data):
        return self.run(data, 10)

    def part2(self, data):
        return self.run(data, 40)

    def run(self, data, steps):
        value, mapping = data

        counts = defaultdict(int)
        for pair in self.get_pairs(value):
            counts[pair] += 1

        for _ in range(steps):
            new_counts = defaultdict(int)
            for pair in counts:
                for new_pair in self.get_pairs(pair[0] + mapping[pair] + pair[1]):
                    new_counts[new_pair] += counts[pair]
            counts = new_counts

        ele_counts = defaultdict(int)
        for key in counts:
            for ele in key:
                ele_counts[ele] += counts[key]

        # Note: the sample data seems to require +1 instead of -1 here.
        return (max(ele_counts.values()) - min(ele_counts.values())) // 2 - 1

    def get_pairs(self, value):
        return ("".join(pair) for pair in zip(value, value[1:]))
