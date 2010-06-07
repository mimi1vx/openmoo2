import pygame

from lbx import load_surface
from game import *

import get_input

import colony_screen
import colony_build_screen

VIEW_SIZE  = 10

LIST_START = 0
LIST_SIZE  = 0

##
#       DRAW
##
def draw(GAME):
    global SCREEN
    global VIEW_SIZE
    global LIST_START
    global LIST_SIZE

    GUI		= GAME['GUI']
    DISPLAY	= GAME['DISPLAY']
    IMAGES	= GAME['IMAGES']
    PALETTES	= GAME['PALETTES']
    FONTS	= GAME['FONTS']

#    STARS	= GAME['DATA']['stars']
#    PLANETS	= GAME['DATA']['planets']
    COLONIES	= GAME['DATA']['colonies']
    
    PLAYERS	= GAME['DATA']['players']
    ME          = GAME['DATA']['me']

    GUI.draw_screen('COLSUM', DISPLAY)

    my_colonies = []

    for colony_id in COLONIES:
        col = COLONIES[colony_id]
        if (col.get_owner() == ME.get_id()) and (not col.is_outpost()):
#        if (COLONIES[i].owner != 0xff) and (COLONIES[i].is_outpost == 0):
#	    my_colonies.append(COLONIES[i])
            my_colonies.append("%s:%i" % (COLONIES[colony_id].get_name(), colony_id))

    print(my_colonies)

    my_colonies.sort()
    for i in range(len(my_colonies)):
        colony_id = int(my_colonies[i].split(":")[1])
        my_colonies[i] = COLONIES[colony_id]

    LIST_SIZE = len(my_colonies)

    buttons = []

    for i in range(LIST_START, min(LIST_SIZE, LIST_START + VIEW_SIZE)):
        colony = my_colonies[i]
        colony_id	= colony.get_id()
        planet_id	= colony.get_planet_id()

        if planet_id == 0xffff:
            print colony
            continue

        y = 38 + (31 * (i - LIST_START))
        
        buttons.append({'action': "colony", 'colony_id': colony_id, 'rect': pygame.Rect((12, y), (84, 29))})
        buttons.append({'action': "colony_build", 'colony_id': colony_id, 'rect': pygame.Rect((513, y), (82, 29))})

        DISPLAY.blit(FONTS['font_10'].render(colony.get_name(), 1, (0x80, 0xA0, 0xBC)), (12, y + 6))

        for t in (0x02, 0x82, 0x03):
            if t == 0x02:
                x = 101
        	icon = 1
            elif t == 0x82:
                x = 236
            	icon = 3
            elif t == 0x03:
                x = 378
            	icon = 5

            c = len(colony.colonists[t])
            if c < 5:
        	xx = 28
    	    else:
        	xx = 114 / c

    	    for ii in range(c):
                colonist = colony.colonists[t][ii]
                race = colonist['race']
                picture = PLAYERS[race].get_picture()
                DISPLAY.blit(IMAGES['RACEICON.LBX'][picture][icon], (x + (xx * ii), y))

    pygame.display.flip()
    return buttons
# /draw

##
#       RUN
##
def run(GAME):
    global VIEW_SIZE
    global LIST_START
    global LIST_SIZE
    

    triggers = [
        {'action': "ESCAPE",        'rect': pygame.Rect((544, 445), (70, 18))},
        {'action': "SCROLL_UP",      'rect': pygame.Rect((620, 16), (8, 18))},
        {'action': "SCROLL_DOWN",    'rect': pygame.Rect((620, 318), (8, 18))}
    ]

    triggers2 = draw(GAME)

    while True:
        event = get_input.get_input(triggers + triggers2)
        action = event['action']
        
        if (action == "ESCAPE"):
            return

        elif action == "SCROLL_UP":
            if LIST_START > 0:
                LIST_START -= 1
                triggers2 = draw(GAME)

        elif action == "SCROLL_DOWN":
            if LIST_START < (LIST_SIZE - VIEW_SIZE):
                LIST_START += 1
                triggers2 = draw(GAME)

        elif (action == "colony"):
    	    colony_screen.run(GAME, event['colony_id'])
            triggers2 = draw(GAME)

        elif (action == "colony_build"):
    	    colony_build_screen.run(GAME, event['colony_id'])
            triggers2 = draw(GAME)

        else:
            print "UNKNONW ACTION: " + action
