import pygame
from pygame.locals import *

MOUSE_LEFT_BUTTON       = 1
MOUSE_MIDDLE_BUTTON     = 2
MOUSE_RIGHT_BUTTON      = 3
MOUSE_WHEELUP		= 4
MOUSE_WHEELDOWN		= 5

class Input():
    """Input is implemented as a singleton!"""

    class __Singleton:

        __display = None
        __cursor_bg = None
        __cursor = None
        __old_mouse_pos = None
        __mouse_pos = None

        __redraw_mouse_event = pygame.USEREVENT + 1
        __redraw_screen_event = pygame.USEREVENT + 2

        def redraw_mouse_event(self):
            return self.__redraw_mouse_event

        def redraw_screen_event(self):
            return self.__redraw_screen_event

        def set_display(self, surface):
            self.__display = surface

        def set_mouse_cursor(self, surface, pos_shift = (0, 0)):
            self.__cursor = surface
            if surface is None:
                pygame.time.set_timer(self.redraw_mouse_event(), 0)
            else:
                pygame.time.set_timer(self.redraw_mouse_event(), 50)

        def reset_mouse_bg(self, size, pad = ""):
            self.__cursor_bg = pygame.Surface(size)

        def save_mouse_bg(self, pad = ""):
            if self.__cursor:

                if self.__cursor_bg is None:
                    self.reset_mouse_bg(self.__cursor.get_size(), pad + "    ")

                if self.__mouse_pos:
                    bg_area = pygame.Rect(self.__mouse_pos, self.__cursor_bg.get_size())
                    return self.__cursor_bg.blit(self.__display, (0, 0), bg_area)

        def redraw_mouse_bg(self, pad = ""):
            if self.__old_mouse_pos and self.__cursor_bg:
                return self.__display.blit(self.__cursor_bg, self.__old_mouse_pos)


        def force_draw_mouse_cursor(self):
            self.save_mouse_bg("    ")
            self.draw_mouse_cursor("    ")

        def draw_mouse_cursor(self, pad = ""):
            if self.__cursor and self.__mouse_pos:
                return self.__display.blit(self.__cursor, self.__mouse_pos)

        def redraw_mouse_cursor(self):
            if self.__cursor and self.__mouse_pos and (self.__old_mouse_pos != self.__mouse_pos):
                update_rect_list = [self.redraw_mouse_bg("    ")]
                self.__old_mouse_pos = self.__mouse_pos
                update_rect_list.append(self.save_mouse_bg("    "))
                update_rect_list.append(self.draw_mouse_cursor("    "))
                pygame.display.update(update_rect_list)

        def get_event(self, triggers_list):
            event = pygame.event.wait()

            if event.type == self.redraw_mouse_event():
                if self.__mouse_pos:
                    if self.__mouse_pos != self.__old_mouse_pos:
                        self.redraw_mouse_cursor()

            if event.type == self.redraw_screen_event():
                return {'action': "redraw"}

            elif event.type == QUIT:
                return {'action': "QUIT"}

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return {'action': "ESCAPE"}
                else:
                    for trigger in triggers_list:
                        if trigger.has_key("key") and trigger['key'] == event.key:
                            return trigger
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

                    for trigger in triggers_list:
                        if trigger['rect'].collidepoint(event.pos):

                            if event.button == MOUSE_LEFT_BUTTON:
                                trigger['mouse_pos'] = (tmpX, tmpY)
                                return trigger

                            elif event.button == MOUSE_RIGHT_BUTTON:
                                return {'action': "help", 'help': trigger['action']}

            elif event.type == MOUSEMOTION:
                self.__mouse_pos = event.pos
                for trigger in triggers_list:
                    if trigger['rect'].collidepoint(event.pos):
                        return {'action': "hover", 'hover': trigger, 'mouse_pos': self.__mouse_pos}

                return {'action': "MOUSEMOTION", 'mouse_pos': self.__mouse_pos}

            return None

    __instance = None

    def __init__( self ):
        if Input.__instance is None:
            Input.__instance = Input.__Singleton()
            self.__dict__['_Singleton__instance'] = Input.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)
