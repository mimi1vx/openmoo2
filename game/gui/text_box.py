import pygame
import screen

from _game_constants import *

import networking
import gui
import dictionary

class TextBox(screen.Screen):

    def __init__(self):
        screen.Screen.__init__(self)
        self.__x = 139
        self.__y = 150
        self.__title = ""
        self.__content = []

    def set_title(self, title):
        self.__title = title

    def set_content(self, content):
        self.__content = content

    def reset_triggers_list(self):
        screen.Screen.reset_triggers_list(self)
        self.add_trigger({'action': "ESCAPE",    	'rect': pygame.Rect((556, 459), ( 72, 20))})

    def draw(self):

        lines = self.__content
        title = self.__title
        x = self.__x
        y = self.__y

        self.reset_triggers_list()

        """draws a MOO2 textbox of varying size,at position x,y,  big enough to output all strings in lines[] """
        light_text_palette = [0x0, 0x802810, 0xe48820, 0xe46824]
        dark_text_palette = [0x0, 0x440c00, 0xac542c]

        self.add_trigger({'action': "ESCAPE",    	'rect': pygame.Rect((0, 0), ( 640, 480))})

        DISPLAY = gui.GUI.get_display()

        font3 = gui.GUI.get_font('font3')
        font5 = gui.GUI.get_font('font5')

        screen_width, screen_height = 640, 480

        mid_part_width = self.get_image('text_box', 'top').get_width()
        mid_part_height = 10 + 15 * len(lines)

        off_y1 = self.get_image('text_box','top').get_height()
        off_y2 = mid_part_height + off_y1

        y3 = self.get_image('text_box', 'bottom').get_height()

        # kludge? Correction for outsized boxes, where the bottom would have ended up outside of screen area
        bottom_box_boundary = y + mid_part_height + off_y1 +y3
        if( bottom_box_boundary) > screen_height :
            y = y - (bottom_box_boundary - screen_height)

        y1 = y + off_y1
        y2 = y + off_y2

        DISPLAY.blit(self.get_image('text_box', 'top'), (x, y))
        temp_r = pygame.Rect((1, 1),(1 + mid_part_width, 1 + mid_part_height))

        DISPLAY.blit(self.get_image('text_box','middle'), (x, y1), temp_r)

        DISPLAY.blit(self.get_image('text_box','bottom'), (x, y2))

        font5.write_text(DISPLAY, x + 120, y + 20, title, light_text_palette, 1)

        lheight = 40

        for i in range(len(lines)):
        #   TODO: some intelligent way of justifying the lines, so the output resembles the original game
            font3.write_text(DISPLAY, x + 40, y + lheight, lines[i], dark_text_palette, 1)
            lheight += 15


Screen = TextBox()
