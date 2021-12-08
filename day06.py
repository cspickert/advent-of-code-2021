from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        return [int(value) for value in input.split(",")]

    def part1(self, data):
        return self.simulate(data, 80)

    def part2(self, data):
        # return self.simulate(data, 256)
        pass

    def simulate(self, data, days):
        for _ in range(days):
            next_data = []
            for i in range(len(data)):
                if data[i] > 0:
                    next_data.append(data[i] - 1)
                else:
                    next_data.extend((6, 8))
            data = next_data
        return len(data)
