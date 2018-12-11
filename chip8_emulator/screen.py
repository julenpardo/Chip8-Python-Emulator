from threading import Thread
import pygame


class Screen(Thread):

    _WIDTH = 128
    _HEIGHT = 64
    _SCREEN_COLOR_RGB = (0, 0, 0)
    _PIXEL_COLOR_RGB = (255, 255, 255)

    def __init__(self):
        Thread.__init__(self)
        self._init_frame_buffer_to_0()
        self.screen = pygame.display.set_mode((self._WIDTH, self._HEIGHT))

    def _clear_screen(self):
        self.screen.fill(self._SCREEN_COLOR_RGB)
        pygame.display.flip()

    def _init_frame_buffer_to_0(self):
        self._frame_buffer = [[0] * self._WIDTH for i in range(self._HEIGHT)]

    def _set_bit_row_to_frame_buffer(self, bit_row_string, buffer_row_y_axis,
                                     buffer_column_x_axis):
        for bit_column_string in bit_row_string:
            bit_column_int = int(bit_column_string)
            if buffer_row_y_axis >= self._HEIGHT:
                buffer_row_y_axis = buffer_row_y_axis - self._HEIGHT
            if buffer_column_x_axis >= self._WIDTH:
                buffer_column_x_axis = buffer_column_x_axis - self._WIDTH
            self._frame_buffer[buffer_row_y_axis][buffer_column_x_axis] ^= bit_column_int
            buffer_column_x_axis += 1

    def _update_frame_buffer(self, sprite, buffer_row_y_axis,
                             buffer_column_x_axis):
        for pixel_int_row in sprite:
            bit_row_string = '{:08b}'.format(pixel_int_row)
            self._set_bit_row_to_frame_buffer(bit_row_string,
                                              buffer_row_y_axis,
                                              buffer_column_x_axis)
            buffer_row_y_axis += 1

    def _draw_pixel(self, x, y):
        pygame.draw.line(self.screen, self._PIXEL_COLOR_RGB, (x, y), (x, y))

    def _refresh(self):
        buffer_row_y_axis = 0
        for row in self._frame_buffer:
            buffer_column_x_axis = 0
            for column in row:
                if self._frame_buffer[buffer_row_y_axis][buffer_column_x_axis]:
                    self._draw_pixel(buffer_column_x_axis, buffer_row_y_axis)
                buffer_column_x_axis += 1
            buffer_row_y_axis += 1

        pygame.display.flip()

    def draw_sprite(self, sprite, buffer_column_x_axis, buffer_row_y_axis):
        self._clear_screen()
        self._update_frame_buffer(sprite, buffer_row_y_axis,
                                  buffer_column_x_axis)
        self._refresh()

    def run(self):
        print('Thread started')
