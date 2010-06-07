
__author__="peterman"
__date__ ="$Jan 7, 2009 8:44:49 PM$"

import pygame
from pygame.locals import *

MOUSE_LEFT_BUTTON       = 1
MOUSE_MIDDLE_BUTTON     = 2
MOUSE_RIGHT_BUTTON      = 3
MOUSE_WHEELUP		= 4
MOUSE_WHEELDOWN		= 5

def get_input(triggers):

    tmpX, tmpY = 0, 0
    while True:

        events = pygame.event.get()

        for event in events:

#            print event

            if (event.type == QUIT):
                return {'action': "QUIT"}

            elif (event.type == KEYDOWN):
                if (event.key == 27):
                    return {'action': "ESCAPE"}
                else:
                    return {'action': "key", 'key': event.key}

            elif (event.type == MOUSEBUTTONDOWN):

                if event.button == MOUSE_MIDDLE_BUTTON:
                    print event

                elif event.button == MOUSE_WHEELUP:
                    return {'action': "SCROLL_UP"}

                elif event.button == MOUSE_WHEELDOWN:
                    return {'action': "SCROLL_DOWN"}

                else:
            	    tmpX, tmpY = event.pos[0], event.pos[1]

            	    for trigger in triggers:
                	if trigger['rect'].collidepoint(event.pos):

                    	    if event.button == MOUSE_LEFT_BUTTON:
                        	return trigger

                    	    elif event.button == MOUSE_RIGHT_BUTTON:
#                        	return "help:" + button['action']
                        	return {'action': "help", 'help': trigger['action']}

            elif event.type == MOUSEMOTION:
                tmpX, tmpY = event.pos[0], event.pos[1]
                for trigger in triggers:
                    if trigger['rect'].collidepoint(event.pos):
                        return {'action': "hover", 'hover': trigger}