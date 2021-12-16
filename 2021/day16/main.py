from typing import List
from math import prod
from functools import reduce

class Packet:

    HEX2BIN = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'A': '1010',
        'B': '1011',
        'C': '1100',
        'D': '1101',
        'E': '1110',
        'F': '1111'
    }

    def __init__(self, hex_str: str='', bin_str: str='') -> None:
        self.bin = bin_str if hex_str == '' else self.__conv_to_bin(hex_str)
        self.subpackets = [] # type: List['Packet']
        self.version = self.__get_version()
        self.type = self.__get_type()
        if self.type == 4:
            self.literal_value = self.__get_literal_value()
        else:
            self.lengthtype = self.__get_length_type()
            if self.lengthtype == 0:
                self.tot_length = self.__get_tot_length()
                self.residual_bin = self.bin[22+self.tot_length:]
                self.__process_subpackets_len(self.bin[22:22+self.tot_length])
            else:
                self.subpacket_count = self.__get_subpacket_count()
                self.__process_subpackets_count(self.bin[18:], self.subpacket_count)

    def __conv_to_bin(self, hex_str: str) -> str:
        return reduce(lambda a, b: a + self.HEX2BIN[b], hex_str, '')

    def __process_subpackets_len(self, bin_str: str) -> None:
        while bin_str != '':
            subpacket = Packet(bin_str = bin_str)
            self.subpackets.append(subpacket)
            bin_str = subpacket.residual_bin

    def __process_subpackets_count(self, bin_str: str, count: int) -> None:
        for _ in range(count):
            subpacket = Packet(bin_str = bin_str)
            self.subpackets.append(subpacket)
            bin_str = subpacket.residual_bin
        self.residual_bin = bin_str

    def __get_version(self) -> int:
        part = self.bin[:3]
        return int('0b'+part, 2)

    def __get_type(self) -> int:
        part = self.bin[3:6]
        return int('0b'+part, 2)

    def __get_length_type(self) -> int:
        part = self.bin[6]
        return int('0b'+part, 2)

    def __get_tot_length(self) -> int:
        part = self.bin[7:22]
        return int('0b'+part, 2)

    def __get_subpacket_count(self) -> int:
        part = self.bin[7:18]
        return int('0b'+part, 2)

    def __get_literal_value(self) -> int:
        pos = 6
        bit = '1'
        bin_tmp = ''
        while bit == '1':
            bit = self.bin[pos]
            bin_tmp += self.bin[pos+1:pos+5]
            pos += 5
        self.residual_bin = self.bin[pos:]
        return int('0b'+bin_tmp, 2)

    def get_version_sum(self) -> int:
        return sum(package.get_version_sum() for package in self.subpackets) + self.version
        #return reduce(lambda s, p: s + p.get_version_sum(), self.subpackets, self.version)

    def process_packet(self) -> int:
        output = 0
        if self.type == 0:
            # sum
            output = sum(packet.process_packet() for packet in self.subpackets)
        elif self.type == 1:
            # product
            output = prod(packet.process_packet() for packet in self.subpackets)
        elif self.type == 2:
            # min
            output = min(packet.process_packet() for packet in self.subpackets)
        elif self.type == 3:
            # max
            output = max(packet.process_packet() for packet in self.subpackets)
        elif self.type == 4:
            # literal value
            output = self.literal_value
        else:
            packet1 = self.subpackets[0].process_packet()
            packet2 = self.subpackets[1].process_packet()
        if self.type == 5:
            # greter than
            output = 1 if packet1 > packet2 else 0
        elif self.type == 6:
            # less than
            output = 1 if packet1 < packet2 else 0
        elif self.type == 7:
            # equals
            output = 1 if packet1 == packet2 else 0
        return output

#Test Cases
P = Packet('D2FE28')
assert P.version == 6
assert P.type == 4
assert P.literal_value == 2021

P = Packet('38006F45291200')
assert P.version == 1
assert P.type == 6
assert P.lengthtype == 0
assert P.tot_length == 27
assert P.subpackets[0].literal_value == 10
assert P.subpackets[1].literal_value == 20

P = Packet('EE00D40C823060')
assert P.version == 7
assert P.type == 3
assert P.lengthtype == 1
assert P.subpacket_count == 3
assert P.subpackets[0].literal_value == 1
assert P.subpackets[1].literal_value == 2
assert P.subpackets[2].literal_value == 3

P = Packet('8A004A801A8002F478')
assert P.version == 4
assert len(P.subpackets) == 1
assert P.subpackets[0].version == 1
assert len(P.subpackets[0].subpackets) == 1
assert P.subpackets[0].subpackets[0].version == 5
assert len(P.subpackets[0].subpackets[0].subpackets) == 1
assert P.subpackets[0].subpackets[0].subpackets[0].version == 6
assert P.subpackets[0].subpackets[0].subpackets[0].type == 4
assert P.get_version_sum() == 16

P = Packet('620080001611562C8802118E34')
assert P.version == 3
assert len(P.subpackets) == 2
assert len(P.subpackets[0].subpackets) == 2
assert len(P.subpackets[1].subpackets) == 2
assert P.subpackets[0].subpackets[0].type == 4
assert P.subpackets[0].subpackets[1].type == 4
assert P.subpackets[1].subpackets[0].type == 4
assert P.subpackets[1].subpackets[1].type == 4
assert P.get_version_sum() == 12

P = Packet('C0015000016115A2E0802F182340')
assert len(P.subpackets) == 2
assert len(P.subpackets[0].subpackets) == 2
assert len(P.subpackets[1].subpackets) == 2
assert P.subpackets[0].subpackets[0].type == 4
assert P.subpackets[0].subpackets[1].type == 4
assert P.subpackets[1].subpackets[0].type == 4
assert P.subpackets[1].subpackets[1].type == 4
assert P.get_version_sum() == 23

P = Packet('A0016C880162017C3686B18A3D4780')
assert len(P.subpackets) == 1
assert len(P.subpackets[0].subpackets) == 1
assert len(P.subpackets[0].subpackets[0].subpackets) == 5
assert P.subpackets[0].subpackets[0].subpackets[0].type == 4
assert P.subpackets[0].subpackets[0].subpackets[1].type == 4
assert P.subpackets[0].subpackets[0].subpackets[2].type == 4
assert P.subpackets[0].subpackets[0].subpackets[3].type == 4
assert P.subpackets[0].subpackets[0].subpackets[4].type == 4
assert P.get_version_sum() == 31

assert Packet('C200B40A82').process_packet() == 3
assert Packet('04005AC33890').process_packet() == 54
assert Packet('880086C3E88112').process_packet() == 7
assert Packet('CE00C43D881120').process_packet() == 9
assert Packet('D8005AC2A8F0').process_packet() == 1
assert Packet('F600BC2D8F').process_packet() == 0
assert Packet('9C005AC2F8F0').process_packet() == 0
assert Packet('9C0141080250320F1802104A08').process_packet() == 1

#Real thing
with open('input.txt', encoding='UTF-8') as file:
    line = file.readline()
line = line.replace('\n', '').strip()
P = Packet(line)
assert P.get_version_sum() == 984
print(P.get_version_sum())
assert P.process_packet() == 1015320896946
print(P.process_packet())
