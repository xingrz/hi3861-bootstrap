#!/usr/bin/env python3
# coding=utf-8

import argparse
import struct


class crc16:
    POLYNOMIAL = 0x1021
    PRESET = 0x0000
    _tab = []

    def __init__(self):
        self._tab = [self._initial(i) for i in range(256)]

    def _initial(self, c):
        crc = 0
        c = c << 8
        for j in range(8):
            if (crc ^ c) & 0x8000:
                crc = (crc << 1) ^ self.POLYNOMIAL
            else:
                crc = crc << 1
            c = c << 1
        return crc

    def _update_crc(self, crc, c):
        cc = 0xff & int(c)

        tmp = (crc >> 8) ^ cc
        crc = (crc << 8) ^ self._tab[tmp & 0xff]
        crc = crc & 0xffff

        return crc

    def crc(self, str):
        crc = self.PRESET
        for c in str:
            crc = self._update_crc(crc, ord(c))
        return crc

    def crcb(self, i):
        crc = self.PRESET
        for c in i:
            crc = self._update_crc(crc, c)
        return crc


def main():
    parser = argparse.ArgumentParser(description='Make file for hiburn')
    parser.add_argument('loader_file', metavar='loader_file',
                        type=str, help='input loader file')
    parser.add_argument('burn_file', metavar='burn_file',
                        type=str, help='input burn file')
    parser.add_argument('packet_file', metavar='output_file',
                        type=str, help='output packet file')
    args = parser.parse_args()

    with open(args.loader_file, 'rb') as f_ldr, open(args.burn_file, 'rb') as f_bin,  open(args.packet_file, 'wb+') as f_out:
        data_ldr = f_ldr.read()
        data_bin = f_bin.read()

        crc = 0

        images_cnt = 2
        header_len = 12 + images_cnt * 52
        total_size = header_len + len(data_ldr) + len(data_bin)

        f_out.write(struct.pack('>I', 0xdfadbeef))
        f_out.write(struct.pack('<HHI', crc, images_cnt, total_size))

        offset = header_len

        f_out.write(struct.pack('<32sIIIII',
                                bytes("loader.bin", 'ascii'),  # path
                                offset,  # offset
                                len(data_ldr),  # image size
                                0,  # burn addr
                                0,  # burn size
                                0  # type
                                )
                    )

        offset += len(data_ldr) + 16

        f_out.write(struct.pack('<32sIIIII',
                                bytes("app.bin", 'ascii'),  # path
                                offset,  # offset
                                len(data_bin),  # image size
                                0,  # burn addr
                                0x200000,  # burn size
                                1  # type
                                )
                    )

        f_out.write(data_ldr)
        f_out.write(struct.pack('<IIII', 0, 0, 0, 0))

        f_out.write(data_bin)
        f_out.write(struct.pack('<IIII', 0, 0, 0, 0))

        f_out.flush()
        f_out.seek(6)

        newdata = f_out.read(header_len - 6)
        crc = crc16().crcb(newdata)
        f_out.seek(4)
        f_out.write(struct.pack('<H', crc))


if __name__ == '__main__':
    main()
