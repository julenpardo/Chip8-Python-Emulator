import unittest
from chip8_emulator.chip8 import Chip8


class Chip8Test(unittest.TestCase):

    def _init_chip8(self, program_counter=0x200, stack_pointer=0xEA0, stack=[],
                    v_registers=[]):
        chip8 = Chip8()
        chip8.program_counter = program_counter
        chip8.stack_pointer = stack_pointer
        chip8.stack = stack
        chip8.v_registers = v_registers

        return chip8

    def test_clear_screen(self):
        """ 00E0"""
        self.fail('Not yet tested')

    def test_ret(self):
        """ 00EE """
        program_counter = 0x317
        stack_pointer = 0xEA2
        stack = [0x201, 0x204, 0x25F]

        chip8 = self._init_chip8(program_counter, stack_pointer, stack)
        chip8.ret()

        expected_program_counter = 0x25F
        actual_program_counter = chip8.program_counter
        expected_stack_pointer = 0xEA1
        actual_stack_pointer = chip8.stack_pointer

        self.assertEqual(expected_program_counter, actual_program_counter)
        self.assertEqual(expected_stack_pointer, actual_stack_pointer)

    def test_jump(self):
        """ 1NNN """
        jump_to = 0x47F

        chip8 = self._init_chip8()
        chip8.jump(jump_to)

        expected = jump_to
        actual = chip8.program_counter

        self.assertEqual(expected, actual)

    def test_call(self):
        """ 2NNN """
        program_counter = 0x617
        stack_pointer = 0xEA3
        stack = [0x351, 0x215, 0x812, 0x4FA]
        call_subroutine_in = 0xBA4

        chip8 = self._init_chip8(program_counter, stack_pointer, stack)
        chip8.call(call_subroutine_in)

        expected_program_counter = call_subroutine_in
        actual_program_counter = chip8.program_counter
        expected_stack_pointer = 0xEA4
        actual_stack_pointer = chip8.stack_pointer
        expected_stack = [0x351, 0x215, 0x812, 0x4FA, 0x617]
        actual_stack = chip8.stack

        self.assertEqual(expected_program_counter, actual_program_counter)
        self.assertEqual(expected_stack_pointer, actual_stack_pointer)
        self.assertEqual(expected_stack, actual_stack)

    def test_skip_next_instruction_if_equals(self):
        """ 3XNN """
        program_counter = 0x31A
        v_registers = [None] * 16
        vx_index = 0x5
        v_registers[vx_index] = 0xAE
        chip8 = self._init_chip8(program_counter, v_registers=v_registers)

        value_to_compare = 0xAE
        chip8.skip_next_instruction_if_equals(vx_index, value_to_compare)

        expected_program_counter = 0x31C
        actual_program_counter = chip8.program_counter

        self.assertEqual(expected_program_counter, actual_program_counter)

    def test_skip_next_instructions_if_not_equals(self):
        """ 4XNN """
        program_counter = 0xBAE
        v_registers = [None] * 16
        vx_index = 0x2
        v_registers[vx_index] = 0x14
        chip8 = self._init_chip8(program_counter, v_registers=v_registers)

        value_to_compare = 0xAE
        chip8.skip_next_instruction_if_not_equals(vx_index, value_to_compare)

        expected_program_counter = 0xBB0
        actual_program_counter = chip8.program_counter

        self.assertEqual(expected_program_counter, actual_program_counter)

    def test_skip_next_instruction_if_vx_equals_vy(self):
        """ 5XY0 """
        self.fail('Not yet tested')

    def test_set_v_fixed_value(self):
        """ 6XNN """
        v_registers = [None] * 16
        vx_index = 0xA
        value = 0xEA
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8.set_v_fixed_value(vx_index, value)

        expected_vx = value
        actual_vx = chip8.v_registers[vx_index]

        self.assertEqual(expected_vx, actual_vx)

    def test_add_to_v(self):
        """ 7XNN """
        vx_index = 0x5
        v_registers = [None] * 16
        v_registers[vx_index] = 0x78
        value_to_add = 0xAF
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8.add_to_v(vx_index, value_to_add)

        expected_vx_value = 0xFD
        actual_vx_value = chip8.v_registers[vx_index]

        self.assertEqual(expected_vx_value, actual_vx_value)

    def test_set_vx_to_vy(self):
        """ 8XY0 """
        vx_index = 0x2
        vy_index = 0x4
        v_registers = [None] * 16
        v_registers[vx_index] = 0xAE
        v_registers[vy_index] = 0x13
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8.set_vx_to_vy(vx_index, vy_index)

        expected_vx_value = 0x13
        actual_vx_value = chip8.v_registers[vx_index]

        self.assertEqual(expected_vx_value, actual_vx_value)

    def test_vx_or_vy(self):
        """ 8XY1 """
        vx_index = 0x2
        vy_index = 0x4
        v_registers = [None] * 16
        v_registers[vx_index] = 0xDE
        v_registers[vy_index] = 0x81
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8.vx_or_vy(vx_index, vy_index)

        expected_vx_value = 0xDF
        actual_vx_value = chip8.v_registers[vx_index]

        self.assertEqual(expected_vx_value, actual_vx_value)

    def test_vx_and_vy(self):
        """ 8XY2 """
        vx_index = 0x3
        vy_index = 0xF
        v_registers = [None] * 16
        v_registers[vx_index] = 0xA8
        v_registers[vy_index] = 0x37
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8.vx_and_vy(vx_index, vy_index)

        expected_vx_value = 0x20
        actual_vx_value = chip8.v_registers[vx_index]

        self.assertEqual(expected_vx_value, actual_vx_value)

    def test_vx_xor_vy(self):
        """ 8XY3 """
        vx_index = 0x4
        vy_index = 0x5
        v_registers = [None] * 16
        v_registers[vx_index] = 0x23
        v_registers[vy_index] = 0x61
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8.vx_xor_vy(vx_index, vy_index)

        expected_vx_value = 0x42
        actual_vx_value = chip8.v_registers[vx_index]

        self.assertEqual(expected_vx_value, actual_vx_value)

    def test_add_vy_to_vx(self):
        """ 8XY4 """
        pass

    def test_subtract_vy_from_vx(self):
        """ 8XY5 """
        pass

    def test_shift_right_vx(self):
        """ 8XY6 """
        pass

    def test_subtract_vy_from_vx_negative(self):
        """ 8XY7 """
        pass

    def test_shift_left_vx(self):
        """ 8XYE """
        pass

    def test_skip_next_instruction_if_vx_not_equals_vy(self):
        """ 9XY0 """
        pass

    def test_set_i_register(self):
        """ ANNN """
        pass

    def test_jump_to_address_plus_v0(self):
        """ BNNN """
        pass

    def test_set_vx_to_random_anded_value(self):
        """ CXNN """
        pass

    def test_draw_sprite_at_coordinate(self):
        """ DXYN """
        pass

    def test_skip_next_instruction_if_pressed_key_equals_vx(self):
        """ EX9E """
        pass

    def test_skip_next_instruction_if_pressed_key_not_equals_vx(self):
        """ EXA1 """
        pass

    def test_set_vx_to_delay_timer(self):
        """ FX07"""
        pass

    def test_wait_for_key_store_value_in_vx(self):
        """ FX0A """
        pass

    def test_set_delay_timer_to_vx(self):
        """ FX15 """
        pass

    def test_set_sound_timer_to_vx(self):
        """ FX18 """
        pass

    def test_add_vx_to_i_register(self):
        """ FX1E """
        pass

    def test_set_i_register_to_location_of_sprite_for_vx(self):
        """ FX29 """
        pass

    def test_store_bcd_of_vx_in_i_register(self):
        """ FX33 """
        pass

    def test_store_from_v0_to_vx_in_i_register(self):
        """ FX55 """
        pass

    def test_read_from_v0_to_vx_in_i_register(self):
        """ Fx65"""
        pass
