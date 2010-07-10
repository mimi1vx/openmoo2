import pygame

from _game_constants import *

from screen import Screen

class InfoScreen(Screen):

    def __init__(self, ui):
        Screen.__init__(self, ui)
	self.__tech_review = "achievements"

    def reset_triggers_list(self):
	Screen.reset_triggers_list(self)
        self.add_trigger({'action': "ESCAPE",    		'rect': pygame.Rect((547, 441), ( 64, 17))})

    def draw(self):
        GAME = self.__GAME
        DATA        = GAME['DATA']
        ME          = DATA['me']
        DISPLAY     = self.get_display()

        DICTIONARY	= GAME['DICTIONARY']

        font3 = self.get_font3()
        font4 = self.get_font4()

        tech_palette = [0x0, 0x082808, 0x0c840c]

        DISPLAY.fill((0, 0, 0))
        DISPLAY.blit(self.get_image('info_screen', 'panel'), (0, 0))

#        DISPLAY.blit(FONTS['font_16_bold'].render(stardate(GAME['DATA']['galaxy']['stardate']), 1, (0x0C, 0x94, 0x0C)), (121, 24))

        DISPLAY.blit(self.get_image('info_screen', 'button', 'history_graph', 'off'), (21, 50))
        DISPLAY.blit(self.get_image('info_screen', 'button', 'tech_review', 'off'), (21, 77))
        DISPLAY.blit(self.get_image('info_screen', 'button', 'race_statistics', 'off'), (21, 102))
        DISPLAY.blit(self.get_image('info_screen', 'button', 'turn_summary', 'off'), (21, 128))
        DISPLAY.blit(self.get_image('info_screen', 'button', 'reference', 'off'), (21, 154))

        # grid behind
        DISPLAY.blit(self.get_image('app_pic', 0), (433, 115))

        # app image
        DISPLAY.blit(self.get_image('app_pic', 155), (433, 115))

        tech_carrets = []

        if self.__tech_review == "achievements":

            # New Construction Types
            items = []
            for tech_id in [TECH_PLANET_CONSTRUCTION, TECH_TITAN_CONTRUCTION, TECH_TRANSPORT, TECH_OUTPOST_SHIP, TECH_FREIGHTERS, TECH_COLONY_SHIP, TECH_COLONY_BASE]:
                if tech_id in ME.get_known_techs():
                    items.append(tech_id)
            if len(items):
                tech_carrets.append({'title': "New Construction Types", 'items': items})

            # Spies
            items = []
            for tech_id in [TECH_TELEPATHIC_TRAINING, TECH_NEURAL_SCANNER, TECH_SPY_NETWORK]:
                if tech_id in ME.get_known_techs():
                    items.append(tech_id)
            if len(items):
                tech_carrets.append({'title': "Spies", 'items': items})

        y = 64
        for carret in tech_carrets:
            if len(carret['items']):
                font4.write_text(DISPLAY, 223, y, carret['title'], tech_palette, 2)
                y += 16
                for item in carret['items']:
                    font3.write_text(DISPLAY, 233, y, DICTIONARY['TECH_LIST'][item]['name'], tech_palette, 2)
                    y += 13
                y += 6

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
