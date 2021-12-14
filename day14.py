from collections import Counter

from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        input = """\
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""
        value, mapping_inputs = input.split("\n\n")
        mapping = dict(line.split(" -> ") for line in mapping_inputs.splitlines())
        return value, mapping

    def part1(self, data):
        value, mapping = data
        for _ in range(10):
            value = self.step(value, mapping)
        return self.analyze(value)

    def part2(self, data):
        pass

    def step(self, value, mapping):
        result = value[0]
        for i in range(len(value)):
            key = value[i - 1 : i + 1]
            if key in mapping:
                result += mapping[key] + value[i]
        return result

    def analyze(self, value):
        counts = Counter(value)
        return max(counts.values()) - min(counts.values())
