from dataclasses import dataclass
from typing import List

from base import BaseSolution


@dataclass
class Packet:
    version: int

    @property
    def version_sum(self):
        return self.version


@dataclass
class Literal(Packet):
    value: int


@dataclass
class Operator(Packet):
    sub_packets: List[Packet]

    @property
    def version_sum(self):
        return super().version_sum + sum(
            sub_packet.version_sum for sub_packet in self.sub_packets
        )


def parse_int(size, input_bits):
    if size < 1:
        raise ValueError(f"Invalid size: {size}")
    if len(input_bits) < size:
        raise ValueError(f"Invalid bits: {input_bits}")
    return int(input_bits[:size], 2), input_bits[size:]


def parse_payload(version, type_id, input_bits):
    if type_id == 4:
        return parse_literal(version, input_bits)
    return parse_operator(version, input_bits)


def parse_literal(version, input_bits):
    value = 0
    while True:
        keep_reading, input_bits = parse_int(1, input_bits)
        next_value, input_bits = parse_int(4, input_bits)
        value = (value << 4) + next_value
        if not keep_reading:
            break
    return Literal(version=version, value=value), input_bits


def parse_operator(version, input_bits):
    length_type_id, input_bits = parse_int(1, input_bits)
    sub_packets = []

    if length_type_id == 0:
        sub_packets_length, input_bits = parse_int(15, input_bits)
        while sub_packets_length > 0:
            sub_packet, remaining_bits = parse_packet(input_bits)
            sub_packets_length -= len(input_bits) - len(remaining_bits)
            input_bits = remaining_bits
            sub_packets.append(sub_packet)

    elif length_type_id == 1:
        num_sub_packets, input_bits = parse_int(11, input_bits)
        for _ in range(num_sub_packets):
            sub_packet, input_bits = parse_packet(input_bits)
            sub_packets.append(sub_packet)

    return Operator(version=version, sub_packets=sub_packets), input_bits


def parse_packet(input_bits):
    version, input_bits = parse_int(3, input_bits)
    type_id, input_bits = parse_int(3, input_bits)
    return parse_payload(version, type_id, input_bits)


def parse_hex_input(input_hex):
    input_value = int(input_hex, 16)
    input_bits = f"{input_value:b}"
    packet, _ = parse_packet(input_bits)
    return packet


class Solution(BaseSolution):
    def load_data(self, input_str):
        packet = parse_hex_input(input_str)
        return packet.version_sum

    def part1(self, data):
        return data

    def part2(self, data):
        pass
