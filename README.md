# c8dasm
A Chip-8 disassembler developed using recursive traversal algorithm.

c8dasm is yet another Chip-8 disassembler. But this one uses recursive traversal algorithm to generate its output.
It makes it more accurate than disassemblers using linear sweep algorithm, and allows it to correctly disassemble unaligned jumps.

## Usage

`./c8dasm.py <path/to/romfile>`

## Installation

You just need to have Python 3.7+ installed on your machine. If you want to run tests, you'll need to install `pytest` with `pip`:

`pip install pytest`

And then run all tests with the following command:

`py.test`

## References

You can find CHIP-8 specification here : http://devernay.free.fr/hacks/chip8/C8TECH10.HTM

## Known issues

Opcode `Bxxx` is not handled properly. However, I disassembled a lot of roms, and it seems that this opcode is rarely used.
