from rom_loader import RomLoader

class DisassemblyWriter:
    
    START_ADDRESS = 0x200
    
    def __init__(self, rom, labels, disassembly):
        self.labels = labels
        self.disassembly = disassembly
        self.romdata = RomLoader.load_rom(rom)
        
    def create_disassembly(self):
        dasm = self.get_disassembly_buffer(self.START_ADDRESS)
        
        print(dasm)
        with open("test.txt", "w") as outfile:
            outfile.write(dasm)

    def get_disassembly_buffer(self, address):
        dasm_buffer = "start:\n"
        
        while address < self.get_end_rom_file():
            dasm_buffer += self.get_label_section(address)
            dasm_buffer += self.get_address_section(address)
            line, address = self.get_inst_section(address)
        
        return dasm_buffer
        
    def get_end_rom_file(self):
        return self.START_ADDRESS + len(self.romdata)

    def get_label_section(self, address):
        result = ""

        if address in self.labels:
            result = "lbl_0x{:04x}:\n".format(address)

        return result

    def get_address_section(self, address):
        return "             0x{:04x}".format(address)

    def get_inst_section(self, address):
        line = ""
        
        if address in self.disassembly:
            line = "     {}\n".format(self.disassembly[address])
            address += 2
        else:
            data = self.romdata[address - self.START_ADDRESS]
            sprite = self.get_sprite_string(data)
            line = "     DB 0x{:02x}    ; {}\n".format(data, sprite[::-1])
            address += 1
        
        return (line, address)

    def get_sprite_string(self, data):
        sprite = ""
        for i in range(8):
            if data & 0x1:
                sprite += "1"
            else:
                sprite += " "
            data = data >> 1
        
        return sprite
    
    def save_disassembly(self, buffer):
        pass