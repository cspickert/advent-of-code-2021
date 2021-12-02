from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        return [
            (direction, int(amount_str))
            for direction, amount_str in (
                line.split(" ") for line in input.splitlines()
            )
        ]

    def part1(self, data):
        h_pos, depth = 0, 0
        for direction, amount in data:
            if direction == "forward":
                h_pos += amount
            elif direction == "down":
                depth += amount
            elif direction == "up":
                depth -= amount
        return h_pos * depth

    def part2(self, data):
        aim = 0
        h_pos, depth = 0, 0
        for direction, amount in data:
            if direction == "forward":
                h_pos += amount
                depth += aim * amount
            elif direction == "down":
                aim += amount
            elif direction == "up":
                aim -= amount
        return h_pos * depth
