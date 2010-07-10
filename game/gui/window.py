import time
import pygame
from pygame.locals import *

MOUSE_LEFT_BUTTON       = 1
MOUSE_MIDDLE_BUTTON     = 2
MOUSE_RIGHT_BUTTON      = 3
MOUSE_WHEELUP		= 4
MOUSE_WHEELDOWN		= 5

class Window():

    __redraw_event = pygame.USEREVENT + 1

    def __init__(self, ui):
#        print("@ @ @ gui_window::Window::__init__()")
        self.set_ui(ui)
        self.reset_triggers_list()

    def log_info(self, message):
        ts = int(time.time())
        print("# INFO %i ... %s" % (ts, message))

    def log_error(self, message):
        ts = int(time.time())
        print("! ERROR %i ... %s" % (ts, message))

    def set_display(self, display):
#        print("@ @ @ gui_window::Window::set_display()")
        self.__display = display

    def get_display(self):
        return self.get_ui().get_display()

    def set_ui(self, ui):
#        print("@ @ @ gui_window::Window::__set_ui()")
        self.__ui = ui

    def get_ui(self):
        return self.__ui

    def get_all_fonts(self):
        return self.__ui.get_all_fonts()

    def get_font(self, font_id):
        return self.__ui.get_font(font_id)

#    def load_image(self, lbx_key, picture_id, picture_frame, palette_key, color_key):
#        return self.get_ui().load_image(lbx_key, picture_id, picture_frame, palette_key, color_key)

    def reset_triggers_list(self):
        self.__triggers = []

    def add_trigger(self, trigger):
        if not trigger.has_key('hover_id'):
            trigger['hover_id'] = None
        self.__triggers.append(trigger)

    def get_triggers_list(self):
        return self.__triggers

    def get_trigger(self, trigger_id):
        return self.__triggers[trigger_id]

    def redraw_event_id(self):
        return self.__redraw_event

    def get_timestamp(self, zoom = 1):
        return int(time.time() * zoom)

    def get_event(self):
        event = pygame.event.wait()

        if event.type == self.redraw_event_id():
            return {'action': "redraw"}

        elif event.type == QUIT:
            return {'action': "QUIT"}

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return {'action': "ESCAPE"}
            else:
                return {'action': "key", 'key': event.key}

        elif event.type == MOUSEBUTTONUP:
            if event.button == MOUSE_LEFT_BUTTON:
                return {'action': "left_mouse_up"}

        elif event.type == MOUSEBUTTONDOWN:

            if event.button == MOUSE_MIDDLE_BUTTON:
                print event

            elif event.button == MOUSE_WHEELUP:
                return {'action': "SCROLL_UP"}

            elif event.button == MOUSE_WHEELDOWN:
                return {'action': "SCROLL_DOWN"}

            else:
                tmpX, tmpY = event.pos[0], event.pos[1]

                for trigger in self.get_triggers_list():
                    if trigger['rect'].collidepoint(event.pos):

                        if event.button == MOUSE_LEFT_BUTTON:
                            trigger['mouse_pos'] = (tmpX, tmpY)
                            return trigger

                        elif event.button == MOUSE_RIGHT_BUTTON:
                            return {'action': "help", 'help': trigger['action']}

        elif event.type == MOUSEMOTION:
            tmpX, tmpY = event.pos[0], event.pos[1]
            for trigger in self.get_triggers_list():
                if trigger['rect'].collidepoint(event.pos):
                    return {'action': "hover", 'hover': trigger, 'mouse_pos': (tmpX, tmpY)}

            # MOUSEMOTION will be implemented later (windows dragging...)
            return {'action': "MOUSEMOTION", 'mouse_pos': (tmpX, tmpY)}

        return None
