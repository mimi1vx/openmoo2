import pygame

from lbx import load_surface
import get_input

#import formulas

from _game_constants import *

import colony_build_screen


def print_summary_item(data, key, title):
    if data.has_key(key) and data[key]:
        print "+     % 6s ... % 25s    +" % (str(data[key]), title)

def draw_planet_background(GUI, DISPLAY, IMAGES, PALETTES, planet_terrain, bg_pic_id):
    bg_pics = [0, 3, 6, 9, 12, 15, 18, 23, 24, 27]
    pic = bg_pics[planet_terrain] + bg_pic_id

    if IMAGES['PLANET_BACKGROUND'][pic] == None:
        print "Lazy load of PLANET_BACKGROUND #%i" % pic
        GUI.load_planet_background(pic)
#	IMAGES['PLANET_BACKGROUND'][pic] = load_surface(LBX['PLANETS.LBX'].read_picture(pic), 0, PALETTES['PLANETS.LBX'])

    DISPLAY.blit(IMAGES['COLONY_SCREEN']['background'], (0, 0))
    DISPLAY.blit(IMAGES['PLANET_BACKGROUND'][pic], (0, 0))

#
#       DRAW
#
def draw(GAME, star, planet, colony):
    GUI		= GAME['GUI']
    DISPLAY     = GAME['DISPLAY']
    IMAGES      = GAME['IMAGES']
    PALETTES	= GAME['PALETTES']
    FONTS	= GAME['FONTS']

    DICTIONARY	= GAME['DICTIONARY']
    
    PLAYERS	= GAME['DATA']['players']

    buttons = []

    print("=== colony_screen::draw() ... star:")
    print("star:")
    print(str(star))
    print("/star")

#    owner = colony.owner
#    colony_name	= "%s %i" % (star['name'], planet['position'])

    draw_planet_background(GUI, DISPLAY, IMAGES, PALETTES, planet.get_terrain(), planet.get_picture())

#    pic = pics[planet['terrain']] + planet['picture']

    DISPLAY.blit(IMAGES['COLONY_SCREEN']['panel'], (0, 0))

#    DISPLAY.blit(IMAGES['COLONY_SCREEN']['planet_arrow'], (6,  31))
#    DISPLAY.blit(IMAGES['COLONY_SCREEN']['planet_arrow'], (6,  55))
#    DISPLAY.blit(IMAGES['COLONY_SCREEN']['planet_arrow'], (6,  79))
#    DISPLAY.blit(IMAGES['COLONY_SCREEN']['planet_arrow'], (6, 103))
#    DISPLAY.blit(IMAGES['COLONY_SCREEN']['planet_arrow'], (6, 127))
    
    for i in range(5):
        object_id = star.get_objects()[i]
        if object_id != 0xFFFF:
            object = GAME['DATA']['planets'][object_id]
            print "type: %i" % object.get_type()

            if object.is_asteroid_belt():
                x = 6
                y = 22 + (24 * i)
                DISPLAY.blit(IMAGES['COLONY_SCREEN']['asteroids_scheme'], (x, y))
                DISPLAY.blit(FONTS['font_10'].render("Asteroids", 1, (0x6C, 0x68, 0x8C)), (x + 30, y + 6))

            if object.is_gas_giant():
                x = 11
                y = 27 + (24 * i)
                DISPLAY.blit(IMAGES['COLONY_SCREEN']['gasgiant_scheme'], (x, y))
                DISPLAY.blit(FONTS['font_10'].render("Gas Giant -", 1, (0x6C, 0x68, 0x8C)), (x + 24, y + 2))
                DISPLAY.blit(FONTS['font_10'].render("uninhabitable", 1, (0x6C, 0x68, 0x8C)), (x + 24, y + 12))

            elif object.is_planet():
                terrain = object.get_terrain()
                size = object.get_size()
                x = 10 + [6, 4, 3, 1, 0][size]
                y = 26 + (24 * i) + [6, 4, 2, 1, 0][size]
                DISPLAY.blit(IMAGES['COLONY_SCREEN']['planet_schemes'][terrain][size], (x, y))
        DISPLAY.blit(IMAGES['COLONY_SCREEN']['planet_arrow'], (6,  31 + (24 * i)))
    
    title = "%s of %s" % (DICTIONARY['COLONY_ASSIGNMENT'][colony.assignment], colony.get_name())
    (tw, th) = FONTS['font_14_bold'].size(title)
    
#    DISPLAY.blit(FONTS['font_16_bold'].render(title, 1, (0x20, 0x28, 0x4c)), (320 - (tw / 2), 1))
#    DISPLAY.blit(FONTS['font_16_bold'].render(title, 1, (0x50, 0x6c, 0x90)), (319 - (tw / 2), 0))
    DISPLAY.blit(FONTS['font_14_bold'].render(title, 1, (0x68, 0x68, 0x88)), (320 - (tw / 2), 1))

#    total_population = (1000 * colony['population']) + colony['pop_raised']
#    print
#    print "	Colony:		%s" % colony.name
#    print "	Population:	%i (+%i)" % (total_population, colony['pop_grow'])
#    print "	Industry:	%i" % colony.industry()
#    print "	Research:	%i" % colony.research()
#    print "	Food (result):	%i (%i)" % (colony.food(), colony.food() - colony.population)
#    print "	Colonists:"

    DISPLAY.blit(IMAGES['GOVERNMENT_ICONS'][PLAYERS[colony.get_owner()].get_racepick_item('goverment')], (310, 32))

    def repeat_draw(target_surface, x, y, source_surface, number, icon_width, break_count, area_width):
#	print pos
#	return
        if number < break_count:
            xx = icon_width
        else:
            xx = int(area_width / number)
        for i in range(int(number)):
            target_surface.blit(source_surface, (x, y))
            x += xx
        return x
    # end func repeat_draw
    repeat_draw(DISPLAY, 340, 35, IMAGES['MORALE_ICONS']['good'], colony.morale() // 10, 30, 7, 155)

    x = 10 + repeat_draw(DISPLAY, 128, 64, IMAGES['COLONY2.LBX']['10food'], colony.get_food() // 10, 20, 6, 98)
    repeat_draw(DISPLAY, x, 64, IMAGES['COLONY2.LBX']['1food'], colony.get_food() % 10, 20, 6, 98)

    # industry icons
    number = (colony.get_industry() // 10) + (colony.get_industry() % 10)
    xx = min(int(round(160 / max(1, number))), 20)
    print "### colony_screen::draw ... industry icons ... number = %i, xx = %i" % (number, xx)
    x = repeat_draw(DISPLAY, 128, 94, IMAGES['COLONY2.LBX']['10production'], colony.get_industry() // 10, xx, 99, 162)
    repeat_draw(DISPLAY, x, 94, IMAGES['COLONY2.LBX']['1production'], colony.get_industry() % 10, xx, 99, 162)

    # research icons
    
    number = (colony.get_research() // 10) + (colony.get_research() % 10)
    xx = min(int(round(160 / max(1, number))), 20)
    print "### colony_screen::draw ... research icons ... number = %i, xx = %i" % (number, xx)
    x = repeat_draw(DISPLAY, 128, 124, IMAGES['COLONY2.LBX']['10research'], colony.get_research() // 10, xx, 99, 162)
    repeat_draw(DISPLAY, x, 124, IMAGES['COLONY2.LBX']['1research'], colony.get_research() % 10, xx, 99, 162)

#    print colony['colonists']

    for t in (FARMER, WORKER, SCIENTIST):
        c = len(colony.colonists[t])
#	c = 90
#	for i in range(c):
        if c < 7:
            xx = 30
        else:
            xx = 190 / c

        if t == 0x02:
            icon = 1
            y = 62
        elif t == 0x82:
            icon = 3
            y = 92
        elif t == 0x03:
            icon = 5
            y = 122

        for i in range(c):
            Colonist = colony.colonists[t][i]
#	    colonist = colony['colonists'][t][0]
            race = Colonist['race']
            picture = PLAYERS[race].get_picture()
            x = 310 + xx * i
#	    print "		%.2x %.2x %.2x %.2x" % (Colonist['a'], Colonist['b'], Colonist['c'], Colonist['d'])
            DISPLAY.blit(IMAGES['RACEICON.LBX'][picture][icon], (x, y))
            if i == (c - 1):
                xx = 28	# enlarge the Rect of last icon (no other icon is drawn over it...)
            buttons.append({'action': "pick-colonist:%.2x:%i" % (t, (c - i)),    'rect': pygame.Rect((x, y), (xx, 28))})

    x = 0
    for i in range(colony.marines):
        DISPLAY.blit(IMAGES['RACEICON.LBX'][picture][0x07], (x, 450))
        x += 30

    # TODO: count in all races not just owner!
    total_population = (1000 * colony.total_population()) + sum(colony.pop_raised())
    pop_s = "Pop %i,%.3i k (+%i)" % ((total_population // 1000), (total_population % 1000), sum(colony.pop_grow()))

    (tw, th) = FONTS['font_12'].size(pop_s)

    DISPLAY.blit(FONTS['font_12'].render(pop_s, 1, (0x68, 0x68, 0x88)), (639 - tw, 1))
        
    pygame.display.flip()

    return buttons
# end func draw

##
#       RUN
##
def run(GAME, colony_id):
#    draw(GAME)

    DATA	= GAME['DATA']
#    RULES       = DATA['rules']
#    PLAYERS     = DATA['players']

    print
    print "@@@ colony_screen @@@"
#    print "     planet_id: %i" % planet_id

    colony      = DATA['colonies'][colony_id]

    planet_id	= colony.get_planet_id()
    planet      = DATA['planets'][planet_id]

    star_id	= planet.get_star()
    star	= DATA['stars'][star_id]

#    print "colony_screen::run() ... buildings = %s" % colony.buildings
    print "colony_screen::run() ... colony.build_queue[] = %s" % colony.build_queue()[0]
    print "colony_screen::run() ... colony.build_queue[] = %s" % colony.build_queue()[1]
    print "colony_screen::run() ... colony.build_queue[] = %s" % colony.build_queue()[2]
    print "colony_screen::run() ... colony.build_queue[] = %s" % colony.build_queue()[3]
    print "colony_screen::run() ... colony.build_queue[] = %s" % colony.build_queue()[4]
    print "colony_screen::run() ... colony.build_queue[] = %s" % colony.build_queue()[5]
    print "colony_screen::run() ... colony.build_queue[] = %s" % colony.build_queue()[6]

#    colony.recount(RULES, PLAYERS)

#    draw(GAME, planet['terrain'], planet['picture'], "%s %i" % (star['name'], planet['position']))
    

    triggers = [
        {'action': "ESCAPE",    		'rect': pygame.Rect((556, 459), ( 72, 20))},
        {'action': "leaders",   		'rect': pygame.Rect((556, 427), ( 72, 20))},
        {'action': "change_build",    		'rect': pygame.Rect((519, 123), ( 61, 22))},
        {'action': "buy",       		'rect': pygame.Rect((590, 123), ( 37, 22))},
        {'action': "morale_summary",		'rect': pygame.Rect((309,  31), (202, 29))},
        {'action': "bc_summary",		'rect': pygame.Rect((130,  31), (179, 29))},
        {'action': "food_summary",		'rect': pygame.Rect((130,  61), (179, 26))},
        {'action': "industry_summary",		'rect': pygame.Rect((130,  91), (179, 26))},
        {'action': "research_summary",		'rect': pygame.Rect((130, 121), (179, 26))}
    ]

    triggers2 = draw(GAME, star, planet, colony)

    while True:
        event = get_input.get_input(triggers + triggers2)
        action = event['action']

        if (action == "ESCAPE"):
            return

        elif (action == "morale_summary"):
            colony.print_morale_summary()

        elif (action == "bc_summary"):
            colony.print_bc_summary()

        elif (action == "food_summary"):
            colony.print_food_summary()

        elif (action == "industry_summary"):
            colony.print_industry_summary()

        elif (action == "research_summary"):
            colony.print_research_summary()

        elif (action == "change_build"):
            colony_build_screen.run(GAME, colony_id)
            triggers2 = draw(GAME, star, planet, colony)

        else:
            print "UNKNONW ACTION: " + action

# end func run
