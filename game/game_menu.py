
__author__="peterman"
__date__ ="$Jan 7, 2009 8:44:49 PM$"

import pygame
import get_input

import load_game

##
#	DRAW
##

def draw(GAME):

    DISPLAY	= GAME['DISPLAY']
    IMAGES	= GAME['IMAGES']
    
    DISPLAY.blit(IMAGES['GAME_MENU']['main'], (144, 25))

    buttons = []

    pygame.display.flip()
    return buttons
# end func draw

def run(GAME):

    print "### game_menu::run()"

    triggers = [
        {'action': "ESCAPE",           'rect': pygame.Rect((370, 342), (64, 17))},
        {'action': "load_game",         'rect': pygame.Rect((294, 71), (86, 23))}
    ]

    keys = {
        'KEYDOWN:108':          "load_game",        # L
        'KEYDOWN:115':          "save_game"         # S
    }

    draw(GAME)

    while True:
        event = get_input.get_input(triggers)
        action = event['action']

        if keys.has_key(action):
            action = keys[action]

        if action == "ESCAPE":
            return
        elif action == "load_game":
            load_game.run(GAME)
            if GAME['close_game_menu']:
                GAME['close_game_menu'] = False
                return
            else:
                draw(GAME)

        else:
            print "UNKNONW ACTION: " + action

# end func dialog_star_system
