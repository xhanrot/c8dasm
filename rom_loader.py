class RomLoader:
    
    @staticmethod
    def load_rom(rom):
        with open(rom, mode="rb") as romfile:
            return bytearray(romfile.read())
    