import pygame

from screen import Screen

class PlanetsScreen(Screen):

    def __init__(self, ui):
        Screen.__init__(self, ui)

    def reset_triggers_list(self):
        Screen.reset_triggers_list(self)
        self.add_trigger({'action': "ESCAPE", 'rect': pygame.Rect((457, 444), ( 151, 16))})

    def draw(self):
        DISPLAY     = self.get_display()

        DISPLAY.blit(self.get_image('planets_screen', 'panel'), (0, 0))

        self.flip()

    def run(self, GAME):
        self.__GAME = GAME

        self.draw()

        while True:
            event = self.get_event()
            if event:
                action = event['action']

                if action == "ESCAPE":
                    return

                else:
                    pass
