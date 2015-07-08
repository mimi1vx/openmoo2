
__author__="peterman"
__date__ ="$Jan 7, 2009 8:44:49 PM$"

import pygame
import get_input

from datetime import datetime

import savegame

##
#	DRAW
##

def draw(GAME):
    from game import stardate
    print "### load_game::draw()"

    DISPLAY	= GAME['DISPLAY']
    IMAGES	= GAME['IMAGES']
    FONTS	= GAME['FONTS']

    DISPLAY.blit(IMAGES['GAME_MENU']['load_game'], (144, 25))

    color_dark = (0xC8, 0x64, 0x08)
#    color_light = (0xFC, 0x88, 0x00)

    n = 0
    for sg in savegame.list_savegames():
        name = sg['name']
        date = datetime.fromtimestamp(sg['ST_MTIME']).strftime("%b %d, %Y %H:%M")
        y = 46 + (31 * n)
        DISPLAY.blit(FONTS['font_12'].render(name, 1, color_dark), (175, y))
        DISPLAY.blit(FONTS['font_10'].render("Stardate: %s" % stardate(sg['stardate']), 1, color_dark), (175, y + 14))
        DISPLAY.blit(FONTS['font_10'].render(date, 1, color_dark), (275, y + 14))
        n += 1

    buttons = []

    return buttons
# end func draw

#def run(GAME):
#
#    print "### load_game::run()"
#
#    triggers = [
#        {'action': "ESCAPE",           'rect': pygame.Rect((318, 365), ( 63, 16))},
#        {'action': "load:1",           'rect': pygame.Rect((168,  46), (232, 28))},
#        {'action': "load:2",           'rect': pygame.Rect((168,  77), (232, 28))},
#        {'action': "load:3",           'rect': pygame.Rect((168, 108), (232, 28))},
#        {'action': "load:4",           'rect': pygame.Rect((168, 139), (232, 28))},
#        {'action': "load:5",           'rect': pygame.Rect((168, 170), (232, 28))},
#        {'action': "load:6",           'rect': pygame.Rect((168, 201), (232, 28))},
#        {'action': "load:7",           'rect': pygame.Rect((168, 232), (232, 28))},
#        {'action': "load:8",           'rect': pygame.Rect((168, 263), (232, 28))},
#        {'action': "load:9",           'rect': pygame.Rect((168, 294), (232, 28))},
#        {'action': "load:10",           'rect': pygame.Rect((168, 325), (232, 28))}
#    ]
#
#    keys = {
#        'KEYDOWN:49':          "load:1",        # 1
#        'KEYDOWN:50':          "load:2",        # 2
#        'KEYDOWN:51':          "load:3",        # 3
#        'KEYDOWN:52':          "load:4",        # 4
#        'KEYDOWN:53':          "load:5",        # 5
#        'KEYDOWN:54':          "load:6",        # 6
#        'KEYDOWN:55':          "load:7",        # 7
#        'KEYDOWN:56':          "load:8",        # 8
#        'KEYDOWN:57':          "load:9",        # 9
#        'KEYDOWN:48':          "load:10",       # 0
#    }
#
#    draw(GAME)
#
#    while True:
#        event = get_input.get_input(triggers)
#        action = event['action']
#
#        if keys.has_key(action):
#            action = keys[action]
#
#        if action == "ESCAPE":
#            return
#
#        elif (action[:5] == "load:"):
#            filename = "SAVE%i.GAM" % int(action[5:])
#            print "Load game: %s" % filename
#            GAME['DATA'] = savegame.read_savegame(filename)
#            GAME['close_game_menu'] = True
#            return
#
#        else:
#            print "UNKNONW ACTION: " + action
