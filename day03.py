from base import BaseSolution

from collections import Counter


class Solution(BaseSolution):
    def load_data(self, input):
        return [list(line) for line in input.splitlines()]

    def part1(self, data):
        data = zip(*data)
        data = [self.analyze_row(row) for row in data]
        data = zip(*data)
        gamma, epsilon = [int("".join(item), 2) for item in data]
        return gamma * epsilon

    def part2(self, data):
        o2_rating = self.analyze_data(data, 0)
        co2_rating = self.analyze_data(data, 1)
        return o2_rating * co2_rating

    def analyze_data(self, data, i):
        """Takes a 2-D matrix of '0' and '1', and iteratively filters it
        based on either the most (i=0) or least (i=1) frequent value in
        each column on each iteration. Returns the last remaining value
        as an int."""

        for pos in range(len(data[0])):
            tr_data = list(zip(*data))
            target_val = self.analyze_row(tr_data[pos])[i]
            data = [row for row in data if row[pos] == target_val]
            if len(data) == 1:
                break
        return int("".join(data[0]), 2)

    def analyze_row(self, row):
        """Counts the frequencies of '0' and '1' in `row` and returns a
        2-tuple with the most and least frequent value. In the case of a
        tie, returns ('1', '0')."""

        items = Counter(row).items()
        ranked_items = sorted(
            items,
            key=lambda item: tuple(reversed(item)),
            reverse=True,
        )
        return [value for value, _ in ranked_items]
