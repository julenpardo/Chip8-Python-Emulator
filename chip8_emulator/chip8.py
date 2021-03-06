import random
from .screen_proxy import ScreenProxy
from .opcode_parser import parse_operation_and_parameters
from .memory import Memory
from .delay_timer_thread import DelayTimerThread


class Chip8:

    def __init__(self, screen, keyboard):
        self.memory = Memory()
        self.screen_proxy = ScreenProxy(screen)
        self.keyboard = keyboard
        self.delay_timer_thread = DelayTimerThread(self.memory)

    def _00e0(self):
        self.screen_proxy.clear_screen()
        self.memory.increment_program_counter()

    def _00ee(self):
        program_counter = self.memory.pop_from_stack()
        self.memory.program_counter = program_counter
        self.memory.increment_program_counter()

    def _1nnn(self, address):
        self.memory.program_counter = address

    def _2nnn(self, address):
        self.memory.add_to_stack(self.memory.program_counter)
        self.memory.program_counter = address

    def _3xkk(self, v_index, instruction):
        self.memory.increment_program_counter()

        if self.memory.v_registers[v_index] == instruction:
            self.memory.increment_program_counter()

    def _4xkk(self, v_index, instruction):
        self.memory.increment_program_counter()

        if self.memory.v_registers[v_index] != instruction:
            self.memory.increment_program_counter()

    def _5xy0(self, vx_index, vy_index):
        self.memory.increment_program_counter()

        if self.memory.v_registers[vx_index] == self.memory.v_registers[vy_index]:
            self.memory.increment_program_counter()

    def _6xkk(self, v_index, value):
        self.memory.v_registers[v_index] = value
        self.memory.increment_program_counter()

    def _7xkk(self, v_index, value):
        addition_result = self.memory.v_registers[v_index] + value
        addition_result_last_8_bits = addition_result & 0xFF
        self.memory.v_registers[v_index] = addition_result_last_8_bits
        self.memory.increment_program_counter()

    def _8xy0(self, vx_index, vy_index):
        self.memory.v_registers[vx_index] = self.memory.v_registers[vy_index]
        self.memory.increment_program_counter()

    def _8xy1(self, vx_index, vy_index):
        self.memory.v_registers[vx_index] |= self.memory.v_registers[vy_index]
        self.memory.increment_program_counter()

    def _8xy2(self, vx_index, vy_index):
        self.memory.v_registers[vx_index] &= self.memory.v_registers[vy_index]
        self.memory.increment_program_counter()

    def _8xy3(self, vx_index, vy_index):
        self.memory.v_registers[vx_index] ^= self.memory.v_registers[vy_index]
        self.memory.increment_program_counter()

    def _8xy4(self, vx_index, vy_index):
        addition_result = self.memory.v_registers[vx_index] \
            + self.memory.v_registers[vy_index]
        addition_result_last_8_bits = addition_result & 0x0FF
        self.memory.v_registers[vx_index] = addition_result_last_8_bits
        self.memory.v_registers[0xF] = 0x00 if addition_result <= 0xFF else 0x01

        self.memory.increment_program_counter()

    def _8xy5(self, vx_index, vy_index):
        vx_value = self.memory.v_registers[vx_index]
        vy_value = self.memory.v_registers[vy_index]

        self.memory.v_registers[0xF] = 0x01 if vx_value > vy_value else 0x00

        subtraction_result_abs = abs(vx_value - vy_value)
        self.memory.v_registers[vx_index] = subtraction_result_abs

        self.memory.increment_program_counter()

    def _8xy6(self, vx_index):
        vx_value = self.memory.v_registers[vx_index]
        vx_last_bit = vx_value & 0x01
        right_shifted_vx_value = vx_value >> 1
        self.memory.v_registers[vx_index] = right_shifted_vx_value
        self.memory.v_registers[0xF] = vx_last_bit

        self.memory.increment_program_counter()

    def _8xy7(self, vx_index, vy_index):
        vx_value = self.memory.v_registers[vx_index]
        vy_value = self.memory.v_registers[vy_index]

        self.memory.v_registers[0xF] = 0x01 if vy_value > vx_value else 0x00

        subtraction_result_abs = abs(vy_value - vx_value)
        self.memory.v_registers[vx_index] = subtraction_result_abs

        self.memory.increment_program_counter()

    def _8xye(self, vx_index):
        vx_value = self.memory.v_registers[vx_index]
        vx_last_bit = vx_value & 0x01
        left_shifted_vx_value = vx_value << 1
        self.memory.v_registers[vx_index] = left_shifted_vx_value
        self.memory.v_registers[0xF] = vx_last_bit

        self.memory.increment_program_counter()

    def _9xy0(self, vx_index, vy_index):
        self.memory.increment_program_counter()

        if self.memory.v_registers[vx_index] != self.memory.v_registers[vy_index]:
            self.memory.increment_program_counter()

    def _annn(self, value):
        self.memory.i_register = value
        self.memory.increment_program_counter()

    def _bnnn(self, address):
        self.memory.program_counter = address + self.memory.v_registers[0x0]

    def _cxkk(self, vx_index, value):
        self.memory.v_registers[vx_index] = random.getrandbits(8) & value
        self.memory.increment_program_counter()

    def _dxyn(self, vx_index, vy_index, sprite_height):
        x_coordinate = self.memory.v_registers[vx_index]
        y_coordinate = self.memory.v_registers[vy_index]
        sprite_address_start = self.memory.i_register
        sprite_address_end = sprite_address_start + sprite_height
        sprite = self.memory.program_memory[sprite_address_start:sprite_address_end]
        self.screen_proxy.draw_sprite(sprite, x_coordinate, y_coordinate)
        self.memory.v_registers[0xF] = self.screen_proxy.collision
        self.memory.increment_program_counter()

    def _ex9e(self, vx_index):
        self.memory.increment_program_counter()

        if self.memory.v_registers[vx_index] == self.keyboard.get_pressed_key():
            self.memory.increment_program_counter()

    def _exa1(self, vx_index):
        self.memory.increment_program_counter()

        if self.memory.v_registers[vx_index] != self.keyboard.get_pressed_key():
            self.memory.increment_program_counter()

    def _fx07(self, vx_index):
        self.memory.set_v_value_to_delay_timer(vx_index)
        self.memory.increment_program_counter()

    def _fx0a(self, vx_index):
        key = self.keyboard.wait_for_key()
        self.memory.v_registers[vx_index] = key
        self.memory.increment_program_counter()

    def _fx15(self, vx_index):
        self.memory.set_delay_timer_to_v_value(vx_index)
        self.memory.increment_program_counter()

    def _fx18(self, vx_index):
        self.memory.set_sound_timer_to_v_value(vx_index)
        self.memory.increment_program_counter()

    def _fx1e(self, vx_index):
        self.memory.i_register += self.memory.v_registers[vx_index]
        self.memory.increment_program_counter()

    def _fx29(self, vx_index):
        sprite_value = self.memory.v_registers[vx_index]
        sprite_address = self.memory.get_address_of_preloaded_sprite(sprite_value)
        self.memory.i_register = sprite_address
        self.memory.increment_program_counter()

    def _fx33(self, vx_index):
        vx_value = '{:03}'.format(self.memory.v_registers[vx_index])
        vx_value_digits = [int(digit) for digit in str(vx_value)]
        addresses = self.memory.get_addresses_from_i_register_to_offset(3)

        for address in addresses:
            self.memory.program_memory[address] = vx_value_digits.pop(0)

        self.memory.increment_program_counter()

    def _fx55(self, vx_index):
        addresses = self.memory.get_addresses_from_i_register_to_offset(
            vx_index + 1)
        v_register_values = self.memory.v_registers[:vx_index + 1]

        for address in addresses:
            self.memory.program_memory[address] = v_register_values.pop(0)

        self.memory.increment_program_counter()

    def _fx65(self, vx_index):
        addresses = self.memory.get_addresses_from_i_register_to_offset(
            vx_index + 1)

        for v_index in range(0, vx_index + 1):
            address = addresses.pop(0)
            self.memory.v_registers[v_index] = self.memory.program_memory[address]

        self.memory.increment_program_counter()

    def _execute_operation(self, operation, parameters):
        # @TODO: refactor operation calling
        operation_name_in_class = '_' + operation
        operation_function = getattr(self, operation_name_in_class)
        if operation_name_in_class.startswith('_00'):
            operation_function()
        elif operation_name_in_class.startswith('_0') \
                or operation_name_in_class.startswith('_1') \
                or operation_name_in_class.startswith('_2') \
                or operation_name_in_class.startswith('_a') \
                or operation_name_in_class.startswith('_b') \
                or operation_name_in_class.startswith('_e') \
                or operation_name_in_class.startswith('_f') \
                or operation_name_in_class.startswith('_8xy6') \
                or operation_name_in_class.startswith('_8xye'):
            operation_function(parameters[0])
        elif operation_name_in_class.startswith('_3') \
                or operation_name_in_class.startswith('_4') \
                or operation_name_in_class.startswith('_5') \
                or operation_name_in_class.startswith('_6') \
                or operation_name_in_class.startswith('_7') \
                or operation_name_in_class.startswith('_8') \
                or operation_name_in_class.startswith('_9') \
                or operation_name_in_class.startswith('_c'):
            operation_function(parameters[0], parameters[1])
        elif operation_name_in_class.startswith('_d'):
            operation_function(parameters[0], parameters[1], parameters[2])

    def _get_rom_bytes(self, rom_path):
        with open(rom_path, 'rb') as rom_handle:
            rom_bytes = rom_handle.read()

        return rom_bytes

    def _initialize(self, rom_path):
        self.memory.load_rom(self._get_rom_bytes(rom_path))
        self.screen_proxy.init_screen()
        self.delay_timer_thread.start()

    def _mainloop(self):
        opcode = self.memory.get_current_opcode()
        operation, parameters = parse_operation_and_parameters(opcode)
        self._execute_operation(operation, parameters)
        self.keyboard.listen()

    def main(self, rom_path):
        self._initialize(rom_path)

        while True:
            self._mainloop()
