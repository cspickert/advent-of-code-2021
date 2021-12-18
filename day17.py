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
        pass
