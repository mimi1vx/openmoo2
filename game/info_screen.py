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
def draw(GAME, tech_review):
    from game import stardate

    DATA        = GAME['DATA']
#    RULES       = DATA['rules']
    ME          = DATA['me']


    DISPLAY     = GAME['DISPLAY']
    IMAGES      = GAME['IMAGES']
    FONTS	= GAME['FONTS']

    DICTIONARY	= GAME['DICTIONARY']
    
#    PLAYERS	= GAME['DATA']['players']

    DISPLAY.fill((0, 0, 0))
#    DISPLAY.fill((0x08, 0x38, 0x08))
    DISPLAY.blit(IMAGES['INFO_SCREEN']['panel'], (0, 0))

    DISPLAY.blit(FONTS['font_16_bold'].render(stardate(GAME['DATA']['galaxy']['stardate']), 1, (0x0C, 0x94, 0x0C)), (121, 24))

    DISPLAY.blit(IMAGES['INFO_SCREEN']['history_graph_off'], (21, 50))
    DISPLAY.blit(IMAGES['INFO_SCREEN']['tech_review_off'], (21, 77))
    DISPLAY.blit(IMAGES['INFO_SCREEN']['race_statistics_off'], (21, 102))
    DISPLAY.blit(IMAGES['INFO_SCREEN']['turn_summary_off'], (21, 128))
    DISPLAY.blit(IMAGES['INFO_SCREEN']['reference_off'], (21, 154))
#    DISPLAY.blit(IMAGES['INFO_SCREEN']['return'], (535, 434))

    DISPLAY.blit(IMAGES['APP_PICS'][0], (433, 115))
    DISPLAY.blit(IMAGES['APP_PICS'][155], (433, 115))

    buttons = []

    tech_carrets = []

    if tech_review == "achievements":

        # New Construction Types
        items = []
        for tech_id in [TECH_TRANSPORT, TECH_OUTPOST_SHIP, TECH_FREIGHTERS, TECH_COLONY_SHIP, TECH_COLONY_BASE]:
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

    y = 63
    for carret in tech_carrets:
        if len(carret['items']):
            DISPLAY.blit(FONTS['font_12_bold'].render(carret['title'], 1, (0x0C, 0x94, 0x0C)), (223, y))
            y += 14
            for item in carret['items']:
                DISPLAY.blit(FONTS['font_12'].render(DICTIONARY['TECH_LIST'][item], 1, (0x0C, 0x94, 0x0C)), (233, y))
                y += 13
            y += 8


    pygame.display.flip()

    return buttons
# end func draw

##
#       RUN
##
def run(GAME):
    global TECH_REVIEW

    if TECH_REVIEW is None:
        TECH_REVIEW = "achievements"

    print
    print "### info_screen::run()"

    triggers = [
        {'action': "ESCAPE",    		'rect': pygame.Rect((547, 441), ( 64, 17))},
    ]

    triggers2 = draw(GAME, TECH_REVIEW)

    while True:
        event = get_input.get_input(triggers + triggers2)
        action = event['action']

        if (action == "ESCAPE"):
            return

        else:
            print "UNKNONW ACTION: " + action

# end func run
