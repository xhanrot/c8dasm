import pytest
from disassembler import Disassembler

@pytest.fixture
def dasm():
    return Disassembler()


def test_simple_decode(dasm):
    rom = [0x00, 0xE0, 0x62, 0xF0, 0x87, 0x20, 0x00, 0xEE]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'CLS',
        0x202: 'LD V2, 0xf0',
        0x204: 'LD V7, V2',
        0x206: 'RET'
        }


def test_simple_decode_with_jump(dasm):
    rom = [0x00, 0xE0, 0x60, 0x04, 0x30, 0x34, 0x12, 0x0A, 0x70, 0x02, 0x61, 0x40]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200:  'CLS',
        0x202:  'LD V0, 0x04',
        0x204:  'SE V0, 0x34',
        0x206:  'JP lbl_0x020a',
        0x208:  'ADD V0, 0x02',
        0x20A:  'LD V1, 0x40'
        }


def test_with_odd_jumps(dasm):
    rom = [0x12, 0x05, 0x00, 0x00, 0x00, 0x60, 0x04]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'JP lbl_0x0205',
        0x205: 'LD V0, 0x04'
    }