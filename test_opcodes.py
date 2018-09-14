import pytest
from disassembler import Disassembler


@pytest.fixture
def dasm():
    return Disassembler()


def test_E0(dasm):
    rom = [0x00, 0xe0]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'CLS'
    }


def test_EE(dasm):
    rom = [0x00, 0xee]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'RET'
    }


def test_1nnn(dasm):
    rom = [0x12, 0x02]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'JP lbl_0x0202'
    }


def test_2nnn(dasm):
    rom = [0x22, 0x02]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'CALL lbl_0x0202'
    }


def test_3xkk(dasm):
    rom = [0x32, 0x0a]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'SE V2, 0x0a'
    }


def test_4xkk(dasm):
    rom = [0x42, 0x0a]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'SNE V2, 0x0a'
    }


def test_5xy0(dasm):
    rom = [0x52, 0x30]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'SE V2, V3'
    }


def test_6xkk(dasm):
    rom = [0x67, 0x03]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'LD V7, 0x03'
    }


def test_7xkk(dasm):
    rom = [0x73, 0x0d]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'ADD V3, 0x0d'
    }


def test_8xy0(dasm):
    rom = [0x83, 0x40]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'LD V3, V4'
    }


def test_8xy1(dasm):
    rom = [0x83, 0x41]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'OR V3, V4'
    }


def test_8xy2(dasm):
    rom = [0x83, 0x42]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'AND V3, V4'
    }


def test_8xy3(dasm):
    rom = [0x83, 0x43]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'XOR V3, V4'
    }


def test_8xy4(dasm):
    rom = [0x83, 0x44]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'ADD V3, V4'
    }


def test_8xy5(dasm):
    rom = [0x83, 0x45]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'SUB V3, V4'
    }


def test_8xy6(dasm):
    rom = [0x83, 0x46]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'SHR V3, V4'
    }


def test_8xy7(dasm):
    rom = [0x83, 0x47]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'SUBN V3, V4'
    }


def test_8xyE(dasm):
    rom = [0x83, 0x4e]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'SHL V3, V4'
    }


def test_9xy0(dasm):
    rom = [0x93, 0x40]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'SNE V3, V4'
    }


def test_Annn(dasm):
    rom = [0xa2, 0x02]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'LD I, lbl_0x0202'
    }


def test_Bnnn(dasm):
    rom = [0xb2, 0x02]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'JP V0, lbl_0x0202'
    }


def test_Cxkk(dasm):
    rom = [0xc5, 0x0e]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'RND V5, 0x0e'
    }


def test_Dxyn(dasm):
    rom = [0xd3, 0x47]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'DRW V3, V4, 0x07'
    }


def test_Ex9E(dasm):
    rom = [0xe3, 0x9e]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'SKP V3'
    }


def test_ExA1(dasm):
    rom = [0xE3, 0xa1]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'SKNP V3'
    }


def test_Fx07(dasm):
    rom = [0xf3, 0x07]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'LD V3, DT'
    }


def test_Fx0A(dasm):
    rom = [0xf3, 0x0a]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'LD V3, K'
    }


def test_Fx15(dasm):
    rom = [0xf3, 0x15]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'LD DT, V3'
    }


def test_Fx18(dasm):
    rom = [0xf3, 0x18]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'LD ST, V3'
    }


def test_Fx1E(dasm):
    rom = [0xf3, 0x1e]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'ADD I, V3'
    }


def test_Fx29(dasm):
    rom = [0xf3, 0x29]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'LD F, V3'
    }


def test_Fx33(dasm):
    rom = [0xf3, 0x33]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'LD B, V3'
    }


def test_Fx55(dasm):
    rom = [0xf3, 0x55]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'LD [I], V3'
    }


def test_Fx65(dasm):
    rom = [0xf3, 0x65]
    dasm.fill_rom(rom)
    dasm.decode(0x200)

    assert dasm.disassembly == {
        0x200: 'LD V3, [I]'
    }
