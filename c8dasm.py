#!/usr/bin/python
import argparse

from disassembler import Disassembler
from disassembly_writer import DisassemblyWriter

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Chip-8 disassembler using traversal tree algorithm.")
    parser.add_argument(
        "romfile",
        help="The rom filename to load"
        )
    args = parser.parse_args()
    
    dasm = Disassembler(args.romfile)
    dasm.decode(0x200)

    writer = DisassemblyWriter(args.romfile, dasm.labels, dasm.disassembly)
    writer.create_disassembly()
    
