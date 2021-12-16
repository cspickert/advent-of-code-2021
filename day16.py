import functools
import operator
from dataclasses import dataclass
from typing import List

from base import BaseSolution


@dataclass
class Packet:
    version: int

    @property
    def version_sum(self):
        return self.version

    def evaluate(self):
        raise NotImplementedError


@dataclass
class Literal(Packet):
    value: int

    def evaluate(self):
        return self.value


@dataclass
class Operator(Packet):
    sub_packets: List[Packet]

    @staticmethod
    def cls_for_type_id(type_id):
        if type_id == 0:
            return Sum
        if type_id == 1:
            return Product
        if type_id == 2:
            return Min
        if type_id == 3:
            return Max
        if type_id == 5:
            return GreaterThan
        if type_id == 6:
            return LessThan
        if type_id == 7:
            return EqualTo
        raise ValueError(f"Unhandled type ID: {type_id}")

    @property
    def version_sum(self):
        return super().version_sum + sum(
            sub_packet.version_sum for sub_packet in self.sub_packets
        )


class Sum(Operator):
    def evaluate(self):
        return sum(sub_packet.evaluate() for sub_packet in self.sub_packets)


class Product(Operator):
    def evaluate(self):
        return functools.reduce(
            operator.mul, (sub_packet.evaluate() for sub_packet in self.sub_packets)
        )


class Min(Operator):
    def evaluate(self):
        return min(sub_packet.evaluate() for sub_packet in self.sub_packets)


class Max(Operator):
    def evaluate(self):
        return max(sub_packet.evaluate() for sub_packet in self.sub_packets)


class GreaterThan(Operator):
    def evaluate(self):
        assert len(self.sub_packets) == 2
        return (
            1 if self.sub_packets[0].evaluate() > self.sub_packets[1].evaluate() else 0
        )


class LessThan(Operator):
    def evaluate(self):
        assert len(self.sub_packets) == 2
        return (
            1 if self.sub_packets[0].evaluate() < self.sub_packets[1].evaluate() else 0
        )


class EqualTo(Operator):
    def evaluate(self):
        assert len(self.sub_packets) == 2
        return (
            1 if self.sub_packets[0].evaluate() == self.sub_packets[1].evaluate() else 0
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
    return parse_operator(version, type_id, input_bits)


def parse_literal(version, input_bits):
    value = 0
    while True:
        keep_reading, input_bits = parse_int(1, input_bits)
        next_value, input_bits = parse_int(4, input_bits)
        value = (value << 4) + next_value
        if not keep_reading:
            break
    return Literal(version=version, value=value), input_bits


def parse_operator(version, type_id, input_bits):
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

    return (
        Operator.cls_for_type_id(type_id)(version=version, sub_packets=sub_packets),
        input_bits,
    )


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
        return parse_hex_input(input_str)

    def part1(self, packet):
        return packet.version_sum

    def part2(self, packet):
        return packet.evaluate()
