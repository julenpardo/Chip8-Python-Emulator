import unittest
from unittest import mock
from chip8_emulator.memory import Memory


class MemoryTest(unittest.TestCase):

    def _init_memory(self, program_memory=[None] * 4096, program_counter=0x200):
        memory = Memory()
        memory.program_memory = program_memory
        memory.program_counter = program_counter

        return memory

    def test_get_current_opcode(self):
        program_memory = [None] * 4096
        program_counter = 0x30F
        loaded_memory_from_0x300 = [
            0x6A, 0x2, 0x6B, 0xC, 0x6C, 0x3F, 0x6D, 0xC, 0xA2, 0xEA,
            0xDA, 0xB6, 0xDC, 0xD6, 0x6E, 0xAE, 0x22, 0xD4, 0x66, 0x3,
            0x68, 0x2, 0x60, 0x60, 0xF0, 0x15, 0xF0, 0x7, 0x30, 0x0,
            0x12, 0x1A, 0xC7, 0x17, 0x77, 0x8, 0x69, 0xFF, 0xA2, 0xF0,
        ]
        program_memory[0x300:0x300] = loaded_memory_from_0x300
        memory = self._init_memory(program_memory, program_counter)

        expected_opcode = bytes([0xAE, 0x22])
        actual_opcode = memory.get_current_opcode()

        self.assertEqual(expected_opcode, actual_opcode)

    def test_load_rom(self):
        memory = self._init_memory()
        rom_path = 'roms/pong.rom'

        with open(rom_path, 'rb') as rom_handle:
            memory.load_rom(rom_handle)

        expected_program_memory = [None] * 4096
        expected_program_memory[0x200:0x200] = [
            0x6A, 0x2, 0x6B, 0xC, 0x6C, 0x3F, 0x6D, 0xC, 0xA2, 0xEA,
            0xDA, 0xB6, 0xDC, 0xD6, 0x6E, 0x0, 0x22, 0xD4, 0x66, 0x3,
            0x68, 0x2, 0x60, 0x60, 0xF0, 0x15, 0xF0, 0x7, 0x30, 0x0,
            0x12, 0x1A, 0xC7, 0x17, 0x77, 0x8, 0x69, 0xFF, 0xA2, 0xF0,
            0xD6, 0x71, 0xA2, 0xEA, 0xDA, 0xB6, 0xDC, 0xD6, 0x60, 0x1,
            0xE0, 0xA1, 0x7B, 0xFE, 0x60, 0x4, 0xE0, 0xA1, 0x7B, 0x2,
            0x60, 0x1F, 0x8B, 0x2, 0xDA, 0xB6, 0x60, 0xC, 0xE0, 0xA1,
            0x7D, 0xFE, 0x60, 0xD, 0xE0, 0xA1, 0x7D, 0x2, 0x60, 0x1F,
            0x8D, 0x2, 0xDC, 0xD6, 0xA2, 0xF0, 0xD6, 0x71, 0x86, 0x84,
            0x87, 0x94, 0x60, 0x3F, 0x86, 0x2, 0x61, 0x1F, 0x87, 0x12,
            0x46, 0x2, 0x12, 0x78, 0x46, 0x3F, 0x12, 0x82, 0x47, 0x1F,
            0x69, 0xFF, 0x47, 0x0, 0x69, 0x1, 0xD6, 0x71, 0x12, 0x2A,
            0x68, 0x2, 0x63, 0x1, 0x80, 0x70, 0x80, 0xB5, 0x12, 0x8A,
            0x68, 0xFE, 0x63, 0xA, 0x80, 0x70, 0x80, 0xD5, 0x3F, 0x1,
            0x12, 0xA2, 0x61, 0x2, 0x80, 0x15, 0x3F, 0x1, 0x12, 0xBA,
            0x80, 0x15, 0x3F, 0x1, 0x12, 0xC8, 0x80, 0x15, 0x3F, 0x1,
            0x12, 0xC2, 0x60, 0x20, 0xF0, 0x18, 0x22, 0xD4, 0x8E, 0x34,
            0x22, 0xD4, 0x66, 0x3E, 0x33, 0x1, 0x66, 0x3, 0x68, 0xFE,
            0x33, 0x1, 0x68, 0x2, 0x12, 0x16, 0x79, 0xFF, 0x49, 0xFE,
            0x69, 0xFF, 0x12, 0xC8, 0x79, 0x1, 0x49, 0x2, 0x69, 0x1,
            0x60, 0x4, 0xF0, 0x18, 0x76, 0x1, 0x46, 0x40, 0x76, 0xFE,
            0x12, 0x6C, 0xA2, 0xF2, 0xFE, 0x33, 0xF2, 0x65, 0xF1, 0x29,
            0x64, 0x14, 0x65, 0x0, 0xD4, 0x55, 0x74, 0x15, 0xF2, 0x29,
            0xD4, 0x55, 0x0, 0xEE, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80,
            0x80, 0x0, 0x0, 0x0, 0x0, 0x0
        ]
        del expected_program_memory[4096:]
        actual_program_memory = memory.program_memory

        self.assertEqual(expected_program_memory, actual_program_memory)
