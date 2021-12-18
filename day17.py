import re

from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input_str):
        return {
            axis: range(int(start), int(end) + 1)
            for axis, start, end in re.findall(r"([xy])=(-?\d+)\.\.(-?\d+)", input_str)
        }

    def part1(self, target_area):
        # Horizontal movement can be ignored since it has no impact on
        # vertical movement. When the probe is at y=0 and falling, it is
        # moving downward at the same speed it was initially launched.
        # From here, we want to find the maximum downward velocity that
        # still causes the probe to land in the target range. The
        # fastest and farthest we can go is all the way to the bottom of
        # the target range in 1 step, so the velocity is equal to the
        # farthest distance within the region from y=0. To get the max
        # height, sum the values from 0 to the velocity.
        return sum(range(-target_area["y"][0]))

    def part2(self, target_area):
        x_velocities = self.find_x_velocities(target_area)
        y_velocities = self.find_y_velocities(target_area)
        return len(
            [
                (dx, dy)
                for dx in x_velocities
                for dy in y_velocities
                if self.probe(target_area, dx, dy)
            ]
        )

    def find_x_velocities(self, target_area):
        x_range = target_area["x"]
        x_velocities = []
        for x_velocity in range(max(x_range), 0, -1):
            x, dx = 0, x_velocity
            while True:
                if x in x_range:
                    x_velocities.append(x_velocity)
                    break
                x += dx
                dx -= 1
                if dx < 0:
                    break
        return set(x_velocities)

    def find_y_velocities(self, target_area):
        y_range = target_area["y"]
        y_velocities = []
        for y_velocity in range(min(y_range), -min(y_range) + 1):
            y, dy = 0, y_velocity
            while True:
                if y in y_range:
                    y_velocities.append(y_velocity)
                    break
                y += dy
                dy -= 1
                if y < min(y_range):
                    break
        return set(y_velocities + [-dy for dy in y_velocities])

    def probe(self, target_area, x_velocity, y_velocity):
        x_range = target_area["x"]
        y_range = target_area["y"]
        x, y = 0, 0

        valid_x_range = range(max(x_range))
        valid_y_range = range(10 ** 10, min(y_range), -1)

        while x in valid_x_range and y in valid_y_range:
            x += x_velocity
            y += y_velocity
            if x_velocity > 0:
                x_velocity -= 1
            y_velocity -= 1
            if x in x_range and y in y_range:
                return True

        return False
