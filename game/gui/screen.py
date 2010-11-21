import pygame
import window

import gui

class Screen(window.Window):

    def __init__(self):
        window.Window.__init__(self)

    def flip(self):
        for trigger in self.get_triggers_list():
            if trigger.has_key('rect'):
#                pygame.draw.rect(self.get_display(), 0xdab1e1, trigger['rect'], 1)
                pass
        self.force_draw_mouse_cursor()
        gui.GUI.flip()

    def attach_screens(self, screens):
        self.__screens = screens

    def get_image(self, img_key, subkey1 = None, subkey2 = None, subkey3 = None):
        return gui.GUI.get_image(img_key, subkey1, subkey2, subkey3)

    def repeat_draw(self, target_surface, x, y, source_surface, number, icon_width, break_count, area_width):
        if number < break_count:
            xx = icon_width
        else:
            xx = int(area_width / number)
        for i in range(int(number)):
            target_surface.blit(source_surface, (x, y))
            x += xx
        return x

    def get_font1(self):
        return self.get_font('font1')

    def get_font2(self):
        return self.get_font('font2')

    def get_font3(self):
        return self.get_font('font3')

    def get_font4(self):
        return self.get_font('font4')

    def get_font5(self):
        return self.get_font('font5')

    def get_font6(self):
        return self.get_font('font6')
