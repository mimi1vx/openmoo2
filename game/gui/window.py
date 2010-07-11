import time
import pygame

import input

class Window():

    def __init__(self, ui):
        self.set_ui(ui)
        self.reset_triggers_list()
        self.__input = input.Input()

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

    def set_redraw_mouse_timer(self, timing):
        pygame.time.set_timer(self.__input.redraw_mouse_event(), timing)

    def set_redraw_screen_timer(self, timing):
        pygame.time.set_timer(self.__input.redraw_screen_event(), timing)

    def set_mouse_cursor(self, surface):
        self.__input.set_mouse_cursor(surface)

    def redraw_mouse_cursor(self):
        self.__input.draw_mouse_cursor()

    def force_draw_mouse_cursor(self):
        self.__input.force_draw_mouse_cursor()

    def get_event(self):
        return self.__input.get_event(self.get_triggers_list())
