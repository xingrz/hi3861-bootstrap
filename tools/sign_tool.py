#!/usr/bin/env python3
# coding=utf-8

import argparse
import struct
import hashlib


def align_up(x, align):
    return (x + align - 1) & ~(align - 1)


def main():
    parser = argparse.ArgumentParser(
        description='Add header and footer to a binary file')
    parser.add_argument('bin_file', metavar='input_file',
                        type=str, help='input binary file')
    parser.add_argument('signed_bin_file', metavar='output_file',
                        type=str, help='output signed binary file')
    args = parser.parse_args()

    with open(args.bin_file, 'rb') as f_in, open(args.signed_bin_file, 'wb') as f_out:
        data = f_in.read()

        # Pad data to 16-byte boundary
        data += bytearray([0] * (align_up(len(data), 16) - len(data)))

        # Add 64-byte header
        header = bytearray()
        header += struct.pack('>I', 0xAA55AA55)
        header += struct.pack('<I', 56)
        header += bytearray([0] * 24)
        header += struct.pack('<I', 64)
        header += struct.pack('<I', len(data))
        header += struct.pack('>I', 0x00003F00)
        header += struct.pack('<I', len(data) + 64)
        header += struct.pack('<I', 32)
        header += struct.pack('>I', 0xCC33CC33)
        header += bytearray([0] * 8)

        # Add 48-byte footer
        footer = bytearray()
        footer += hashlib.sha256(header + data).digest()
        footer += bytearray([0] * 8)
        footer += struct.pack('<I', len(data) + 64 + 48)
        footer += struct.pack('>I', 0xAA55AA55)

        f_out.write(header + data + footer)


if __name__ == '__main__':
    main()
