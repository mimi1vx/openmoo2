import pygame

import get_input

#import formulas

from _game_constants import *

def print_summary_item(data, key, title):
    if data.has_key(key) and data[key]:
        print "+     % 6s ... % 25s    +" % (str(data[key]), title)

TECH_REVIEW = None

##
#       DRAW
##
#def draw(GAME, terrain, picture, colony_name):
def draw(GAME):
    from game import stardate
    DISPLAY     = GAME['DISPLAY']
    IMAGES      = GAME['IMAGES']
#    PALETTES	= GAME['PALETTES']
#    FONTS	= GAME['FONTS']

#    DICTIONARY	= GAME['DICTIONARY']

#    PLAYERS	= GAME['DATA']['players']

    DISPLAY.fill((0, 0, 0))
#    DISPLAY.fill((0x08, 0x38, 0x08))
    DISPLAY.blit(IMAGES['PLANETS_SCREEN']['screen'], (0, 0))

#    DISPLAY.blit(IMAGES['INFO_SCREEN']['return'], (535, 434))

    buttons = []

    pygame.display.flip()

    return buttons
# end func draw

##
#       RUN
##
def run(GAME):

    print
    print "### planets_screen::run()"

    triggers = [
        {'action': "ESCAPE",    		'rect': pygame.Rect((457, 444), ( 151, 16))},
    ]

    triggers2 = draw(GAME)

    while True:
        event = get_input.get_input(triggers + triggers2)
        action = event['action']

        if (action == "ESCAPE"):
            return

        else:
            print "UNKNONW ACTION: " + action

# end func run
