
from rom_loader import RomLoader

class Disassembler:

    START_ADDRESS = 0x200
    
    def __init__(self, rom=None):
        self.romdata = []
        if rom is not None:
            self.romdata = RomLoader.load_rom(rom)
        
        self.labels = []
        self.current_blocks = []
        self.all_blocks = []
        self.disassembly = {}
        
        self.current_address = self.START_ADDRESS
        self.endblock = False
        self.opcodes = {
            0xE0: 'CLS',
            0xEE: 'RET',
            0x1000: 'JP lbl_0x{:04x}',
            0x2000: 'CALL lbl_0x{:04x}',
            0x3000: 'SE V{}, 0x{:02x}',
            0x4000: 'SNE V{}, 0x{:02x}',
            0x5000: 'SE V{}, V{}',
            0x6000: 'LD V{}, 0x{:02x}',
            0x7000: 'ADD V{}, 0x{:02x}',
            0x8000: 'LD V{}, V{}',
            0x8001: 'OR V{}, V{}',
            0x8002: 'AND V{}, V{}',
            0x8003: 'XOR V{}, V{}',
            0x8004: 'ADD V{}, V{}',
            0x8005: 'SUB V{}, V{}',
            0x8006: 'SHR V{}, V{}',
            0x8007: 'SUBN V{}, V{}',
            0x800E: 'SHL V{}, V{}',
            0x9000: 'SNE V{}, V{}',
            0xA000: 'LD I, lbl_0x{:04x}',
            0xB000: 'JP V0, lbl_0x{:04x}',
            0xC000: 'RND V{}, 0x{:02x}',
            0xD000: 'DRW V{}, V{}, 0x{:02x}',
            0xE09E: 'SKP V{}',
            0xE0A1: 'SKNP V{}',
            0xF007: 'LD V{}, DT',
            0xF00A: 'LD V{}, K',
            0xF015: 'LD DT, V{}',
            0xF018: 'LD ST, V{}',
            0xF01E: 'ADD I, V{}',
            0xF029: 'LD F, V{}',
            0xF033: 'LD B, V{}',
            0xF055: 'LD [I], V{}',
            0xF065: 'LD V{}, [I]'
        }

    #  used only for tests
    def fill_rom(self, rom):
        self.romdata = bytearray(rom)

    def decode(self, address):
        self.endblock = False
        self.current_address = address

        while self.endblock is False:
            if self.current_address in self.disassembly:
                self.endblock = True
                break

            if self.current_address - self.START_ADDRESS + 1 > len(self.romdata):
                self.endblock = True
                break

            opcode = self.get_opcode()
            prefix = self.get_prefix(opcode)

            if opcode == 0xE0:
                self.add_disassembly(opcode)
                
            elif opcode == 0xEE:
                self.add_disassembly(opcode)
                self.disassembly[self.current_address] = self.opcodes[opcode]
                self.endblock = True

            elif prefix == 0x1000 or prefix == 0x2000:
                self.endblock = True
                address = self.get_address(opcode)
                self.add_disassembly(prefix, address)
                self.add_label(address)
                self.add_block(address)

            elif prefix == 0x3000 or prefix == 0x4000:
                vx = self.get_vx(opcode)
                byte = self.get_byte(opcode)
                self.add_disassembly(prefix, vx, byte)
                next_address = self.current_address + 4
                self.add_block(next_address)

            elif prefix == 0x5000:
                vx = self.get_vx(opcode)
                vy = self.get_vy(opcode)
                self.add_disassembly(prefix, vx, vy)
                next_address = self.current_address + 4
                self.add_block(next_address)

            elif prefix == 0x6000 or prefix == 0x7000:
                vx = self.get_vx(opcode)
                byte = self.get_byte(opcode)
                self.add_disassembly(prefix, vx, byte)

            elif prefix == 0x8000:
                vx = self.get_vx(opcode)
                vy = self.get_vy(opcode)
                term = self.get_term_8(opcode)
                self.add_disassembly(prefix | term, vx, vy)

            elif prefix == 0x9000:
                vx = self.get_vx(opcode)
                vy = self.get_vy(opcode)
                self.add_disassembly(prefix, vx, vy)
                next_address = self.current_address + 4
                self.add_block(next_address)

            elif prefix == 0xA000:
                address = self.get_address(opcode)
                self.add_disassembly(prefix, address)
                self.add_label(address)

            elif prefix == 0xB000:
                address = self.get_address(opcode)
                self.add_disassembly(prefix, address)
                self.endblock = True
                self.add_block(address)

            elif prefix == 0xC000:
                vx = self.get_vx(opcode)
                byte = self.get_byte(opcode)
                self.add_disassembly(prefix, vx, byte)

            elif prefix == 0xD000:
                vx = self.get_vx(opcode)
                vy = self.get_vy(opcode)
                nibble = opcode & 0xf
                self.add_disassembly(prefix, vx, vy, nibble)

            elif prefix == 0xE000:
                vx = self.get_vx(opcode)
                term = self.get_term_E_F(opcode)
                self.add_disassembly(prefix | term, vx)
                next_address = self.current_address + 4
                self.add_block(next_address)

            elif prefix == 0xF000:
                vx = self.get_vx(opcode)
                term = self.get_term_E_F(opcode)
                self.add_disassembly(prefix | term, vx)

            else:
                print('Unknown opcode: 0x{:04x}'.format(opcode))
                self.endblock = True

            self.current_address += 2

        if len(self.current_blocks) > 0:
            self.decode(self.current_blocks.pop())

    def get_opcode(self):
        return self.romdata[self.current_address - self.START_ADDRESS] << 8 | \
                self.romdata[self.current_address - self.START_ADDRESS + 1]

    def get_prefix(self, opcode):
        return opcode & 0xf000

    def add_disassembly(self, prefix, *args):
        self.disassembly[self.current_address] = self.opcodes[prefix].format(*args)

    def add_block(self, address):
        if address not in self.all_blocks:
            self.current_blocks.append(address)
            self.all_blocks.append(address)

    def add_label(self, address):
        self.labels.append(address)

    def get_vx(self, opcode):
        return (opcode & 0xf00) >> 8

    def get_vy(self, opcode):
        return (opcode & 0xf0) >> 4

    def get_term_8(self, opcode):
        return opcode & 0xf

    def get_term_E_F(self, opcode):
        return opcode & 0xff

    def get_byte(self, opcode):
        return opcode & 0xff

    def get_address(self, opcode):
        return opcode & 0xfff
