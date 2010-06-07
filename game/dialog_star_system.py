
__author__="peterman"
__date__ ="$Jan 7, 2009 8:44:49 PM$"

import pygame
import get_input

import colony_screen
import main_screen

PLANET_TYPE_ASTEROIDS   = 1
PLANET_TYPE_GAS_GIANT   = 2
PLANET_TYPE_PLANET      = 3

COLONY_TYPE_COLONY      = 0
COLONY_TYPE_OUTPOST     = 1

##
#	DRAW
##

def draw(GAME, star_id):

    DISPLAY	= GAME['DISPLAY']
    IMAGES	= GAME['IMAGES']
    FONTS	= GAME['FONTS']
    DICTIONARY	= GAME['DICTIONARY']
    DATA	= GAME['DATA']
    ME          = DATA['me']

    buttons = []

    X, Y = 106, 103
    star = DATA['stars'][star_id]

    print()
    print("@@@ dialog_systemDetail")
    print("     Star: #%i ... %s" % (star_id, star.get_name()))
    print("         Visited: %i" % (star.visited()))
    print()

# dialog window
    DISPLAY.blit(IMAGES['STARSYSTEM_DIALOG'], (X, Y))
# dialog title
    title = "Star System " + star.get_name()
    (tw, th) = FONTS['FONT3'].size(title)

#20284c
#    print star.get_objects()
#    for i in [4, 3, 2, 1, 0]:
    if not star.visited():
        DISPLAY.blit(FONTS['FONT3'].render(title, 1, (0x66, 0x66, 0x66)), (X + 174 - (tw / 2), Y + 14))
    else:
        DISPLAY.blit(FONTS['FONT3'].render(title, 1, (0x20, 0x28, 0x4c)), (X + 175 - (tw / 2), Y + 15))
        DISPLAY.blit(FONTS['FONT3'].render(title, 1, (0x50, 0x6c, 0x90)), (X + 174 - (tw / 2), Y + 14))
        for i in range(5):
            planet_id = star.get_objects()[i]
            print " object_id #%i" % planet_id
            if planet_id != 0xffff:
#               orbit_img_key = "STARSYSTEM_ORBIT%i" % i
                planet = DATA['planets'][planet_id]
                print "		type: %s" % (DICTIONARY['PLANET_TYPES'][planet.get_type()])
                print "		size: %s" % (DICTIONARY['PLANET_SIZES'][planet.get_size()])
                if planet.is_asteroid_belt():
                    if i == 0:
                        DISPLAY.blit(IMAGES['SYSTEM_ASTEROIDS'][i], (X + 30, Y + 60))
                elif planet.is_gas_giant():
                    DISPLAY.blit(IMAGES['SYSTEM_ORBIT'][i], (X + 30, Y + 60))
                elif planet.is_planet():
                    DISPLAY.blit(IMAGES['SYSTEM_ORBIT'][i], (X + 30, Y + 60))
                else:
                    print("WARNING: unknow star system object detected: %i" % (planet.get_type()))

        for i in range(5):
            planet_id = star.get_objects()[i]
            print " object_id #%i" % planet_id
            if planet_id != 0xffff:
                planet = DATA['planets'][planet_id]
                if planet.is_gas_giant():
                    DISPLAY.blit(IMAGES['SYSTEM_GAS_GIANTS'][planet.get_size()], (X + 30 + (60 * i), Y + 60))
                elif planet.is_planet():
#                    terrain = planet['terrain']
#                   print "		name: %s %i" % (planet['parent_star']['name'], i + 1)
#                    print "		gravity: %s" % (DICTIONARY['PLANET_GRAVITIES'][planet.get_gravity()])
 #                   print "		terran: %s" % (DICTIONARY['PLANET_TERRAINS'][planet.get_terrain()])
                    x = X + 30 + (60 * i)
                    y = Y + 60
                    DISPLAY.blit(IMAGES['SYSTEM_PLANETS'][planet.get_terrain()][planet.get_size()], (x, y))
                    colony_id = planet.get_colony_id()
                    if colony_id < 0xffff:
                        colony = DATA['colonies'][colony_id]
#                        print "         colony_id #%i" % colony_id
                        player = DATA['players'][colony.get_owner()]

                        if colony.is_owned_by(ME.get_id()) and colony.is_colony():
 #                           print("colony.population() = %i" % colony.population())
                            pop = str(colony.get_population())
                            buttons.append({'action': "colony", 'colony_id': colony_id, 'rect': pygame.Rect((x, y), (31, 31))})
                        else:
                            pop = ""
                            
                        if colony.is_outpost():
                            DISPLAY.blit(IMAGES['SYSTEM_OUTPOST_MARKS'][player.get_color()], (x - 6, y))
                        else:
# colony['type'] == COLONY_TYPE_COLONY:
                            DISPLAY.blit(IMAGES['SYSTEM_COLONY_MARKS'][player.get_color()], (x - 6, y))
                            DISPLAY.blit(FONTS['font_12'].render(pop, 1, (0xff, 0xff, 0xff)), (x+5, y+5))

#                        print planet
#                        print colony
        DISPLAY.blit(IMAGES['SYSTEM_STAR'][star.get_class()], (X + 160, Y + 120))


#    for terrain in range(10):
#        for size in range(5):
    pygame.display.flip()
    return buttons
# end func draw

def run(GAME, star_id):

    triggers = [
        {'action': "ESCAPE",           'rect': pygame.Rect((370, 342), (64, 17))}
    ] + draw(GAME, star_id)

    while True:
        event = get_input.get_input(triggers)
        action = event['action']

        if action == "ESCAPE":
            return

        elif (action == "colony"):
            colony_screen.run(GAME, event['colony_id'])
            main_screen.draw(GAME)
            draw(GAME, star_id)

        else:
            print "UNKNONW ACTION: " + action

# / end func dialog_star_system
