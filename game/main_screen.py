__author__="peterman"
__date__ ="$Jan 7, 2009 8:44:49 PM$"

if __name__ != "__main__":
    exit

import sys
import pygame

import get_input

from game import stardate

import colonies_screen
import leaders_screen
import dialog_star_system
import game_menu

import info_screen
import research_screen
import planets_screen

import debug

ZOOM_LEVEL = None
map_x, map_y, map_width, map_height = 22, 21, 505, 400

##
#	DRAW
##

def draw_ships(GAME):
    global ZOOM_LEVEL
    global map_x, map_y, map_width, map_height

    PLAYERS = GAME['DATA']['players']
    STARS = GAME['DATA']['stars']
    SHIPS = GAME['DATA']['ships']
    STARS_BY_COORDS = GAME['DATA']['stars_by_coords']

    DISPLAY	= GAME['DISPLAY']
    IMAGES	= GAME['IMAGES']

#    PLAYERS		= GAME['DATA']['players']
#    STARS		= GAME['DATA']['stars']
#    STARS_BY_COORDS	= GAME['DATA']['stars_by_coordinates']
#    SHIPS		= GAME['DATA']['ships']

    galaxy_width, galaxy_height = GAME['DATA']['galaxy']['width'], GAME['DATA']['galaxy']['height']

    for ship_id in SHIPS:
        draw = False
        ship = SHIPS[ship_id]
    	x = map_x + ((ship.get_x() * map_width) / galaxy_width)
    	y = map_y + ((ship.get_y() * map_height) / galaxy_height)
        ship_icon_size = ZOOM_LEVEL
        ship_destination = ship.get_destination()
        if ship.get_owner() < 8:
    	    ship_icon_color = PLAYERS[ship.get_owner()].get_color()
        else:
            ship_icon_color = ship.get_owner()
        ship_icon = IMAGES['MAP_SHIPS'][ship_icon_color][ship_icon_size]

#        ship.print_debug(PLAYERS[ship.get_owner()], STARS)

        if ship.is_orbiting():
            draw = True
            star_class = STARS[ship_destination].get_class()
    	    star_pic_size = 2 - STARS[ship_destination].get_size() + ZOOM_LEVEL
            spic_w, spic_h = IMAGES['MAP_STARS'][star_class][star_pic_size].get_size()
#	    x += 8
#	    y -= 13
            x += spic_w / 3 - 1 - ZOOM_LEVEL
            y -= spic_h / 2
        elif ship.is_travelling():
            draw = True
            ship_w, ship_h = ship_icon.get_size()
            x -= (ship_w / 2) - 4
            y -= (ship_h / 2) - 2
        elif ship.is_launching():
            draw = True
            k = "%i:%i" % (ship.get_x(), ship.get_y())
            star_class = STARS_BY_COORDS[k].get_class()
    	    star_pic_size = 2 - STARS_BY_COORDS[k].get_size() + ZOOM_LEVEL
            spic_w, spic_h = IMAGES['MAP_STARS'][star_class][star_pic_size].get_size()
#    	    star_pic_size = 2 - STARS[ship['location']]['size'] + ZOOM_LEVEL
#	    spic_w, spic_h = IMAGES['MAP_STARS'][star_class][star_pic_size].get_size()
            x -= (spic_w / 2) + 7
            y -= (spic_h / 2) + 1
        if draw:
            DISPLAY.blit(ship_icon, (x, y))
# end func draw_ships

def draw_stars(GAME):
    global ZOOM_LEVEL
    global map_x, map_y, map_width, map_height

    DATA        = GAME['DATA']
    GALAXY      = DATA['galaxy']

    galaxy_width, galaxy_height = GALAXY['width'], GALAXY['height']

    DISPLAY	= GAME['DISPLAY']
    FONTS	= GAME['FONTS']
    IMAGES	= GAME['IMAGES']
    STARS	= GAME['DATA']['stars']

    dynamic_buttons = []

    WORMHOLE_COLOR = 0x242428
#    WORMHOLE_COLOR = 0x663333

    wormholes = {}
    for star_id in STARS.keys():
        star = STARS[star_id]

        # draw the wormholes
        if star.visited():
            if star.wormhole() != 0xff:
                star2 = STARS[star.wormhole()]
                star_ids = [star.get_id(), star2.get_id()]
                key = (min(star_ids) << 8) + max(star_ids)
                if not wormholes.has_key(key):
                    x1, y1 = map_x + ((star.get_x() * map_width) / galaxy_width), map_y + ((star.get_y() * map_height) / galaxy_height)
                    x2, y2 = map_x + ((star2.get_x() * map_width) / galaxy_width), map_y + ((star2.get_y() * map_height) / galaxy_height)
                    wormholes[key] = True

                pygame.draw.line(DISPLAY, WORMHOLE_COLOR, (x1, y1), (x2, y2), 2)

    for star_id in STARS.keys():
        star = STARS[star_id]

        # draw the stars end their names
#    for star in STARS:
        star_class = star.get_class()
        star_size = 2 - star.get_size() + ZOOM_LEVEL
#        print "drawing star '%s' coordinates: [%i, %i], class: %i, size: %i" % (star.get_name(), star.get_x(), star.get_y(), star_class, star_size)

        pic_width = IMAGES['MAP_STARS'][star_class][star_size].get_width()
        pic_height = IMAGES['MAP_STARS'][star_class][star_size].get_height()
        
        x = map_x + ((star.get_x() * map_width) / galaxy_width)
        y = map_y + ((star.get_y() * map_height) / galaxy_height)

#        print " ... [%i, %i]" % (x + xx, y)
        if star_class < 7:
            xx = pic_width / 2
            yy = pic_height / 2
            dynamic_buttons.append({'action': "systemDetail:%i" % star.get_id(), 'rect': pygame.Rect((x - xx, y - yy), (pic_width, pic_height))})
            DISPLAY.blit(IMAGES['MAP_STARS'][star_class][star_size], (x- xx, y - yy))

    for star_id in STARS.keys():
        star = STARS[star_id]
        star_class = star.get_class()
        star_size = 2 - star.get_size() + ZOOM_LEVEL

        pic_width = IMAGES['MAP_STARS'][star_class][star_size].get_width()
        pic_height = IMAGES['MAP_STARS'][star_class][star_size].get_height()

        x = map_x + ((star.get_x() * map_width) / galaxy_width)
        y = map_y + ((star.get_y() * map_height) / galaxy_height)
        yy = pic_height / 2

#        xx = pic_width / 2
#        yy = pic_height / 2

        if star.visited():
            text_width, text_height = FONTS['font_12_bold'].size(star.get_name())
            DISPLAY.blit(FONTS['font_12_bold'].render(star.get_name(), 1, (0x99, 0x99, 0x99)), (x - (text_width / 2), y + yy - 3))
#        else:
#            DISPLAY.blit(FONTS['font_11'].render("BH", 1, (0x33, 0x33, 0x33)), (x - 6, y))

    return dynamic_buttons
# end func draw_stars

def draw(GAME):

    MOO2_DIR = "../moo2"

#    ICON = pygame.image.load(MOO2_DIR + "/orion2-icon.png")
#    pygame.display.set_icon(ICON)

    global ZOOM_LEVEL
    global map_x, map_y, map_width, map_height

    print("GAME.keys = %str" % GAME.keys())

    GUI         = GAME['GUI']

    DATA        = GAME['DATA']

    DISPLAY     = GAME['DISPLAY']
    IMAGES      = GAME['IMAGES']
    FONTS       = GAME['FONTS']

#    RULES       = GAME['rules']

#    PLAYERS     = DATA['players']

    GALAXY      = DATA['galaxy']
#    STARS	= DATA['stars']
#    PLANETS	= DATA['planets']
#    COLONIES	= DATA['colonies']

    galaxy_width, galaxy_height = GALAXY['width'], GALAXY['height']
    galaxy_size_factor = GALAXY['size_factor']

    player		= DATA['me']

    DISPLAY.blit(IMAGES['MAIN_SCREEN']['background'], (0, 0))
    DISPLAY.blit(IMAGES['MAIN_SCREEN']['screen'], (0, 0))

    dynamic_buttons = []

    print "### main_screen::draw() ... galaxy_size_factor = %i" % galaxy_size_factor

#    if ZOOM_LEVEL is None:
    if galaxy_size_factor < 6:
        ZOOM_LEVEL = 4
    elif galaxy_size_factor < 11:
        ZOOM_LEVEL = 3
    elif galaxy_size_factor < 16:
        ZOOM_LEVEL = 2
    elif galaxy_size_factor < 21:
        ZOOM_LEVEL = 1
    else:
        ZOOM_LEVEL = 0
    print "### main_screen::draw() ... ZOOM_LEVEL = %i" % ZOOM_LEVEL

    dynamic_buttons += draw_stars(GAME)
    draw_ships(GAME)

# buzz-rectangle on the main screen star map to check transparent background
#    pygame.draw.rect(DISPLAY, 0x111111, ((map_x, map_y), (map_width, map_height)))

    DISPLAY.blit(FONTS['font_12'].render(stardate(DATA['galaxy']['stardate']), 1, (0xff, 0xff, 0xff)), (558, 27))
#    <Event(5-MouseButtonDown {'button': 2, 'pos': (561, 27)})>

    # BC
    if player.get_bc_income() < 0:
        bc_delta = "%i BC" % player.get_bc_income()
    else:
        bc_delta = "+%i BC" % player.get_bc_income()
    GUI.bordered_text(DISPLAY, "%i BC" % player.get_bc(), (0xff, 0xff, 0xff), (0x00, 0x00, 0x00), 554, 92, FONTS['font_12_bold'])
    GUI.bordered_text(DISPLAY, bc_delta, (0xff, 0xff, 0xff), (0x00, 0x00, 0x00), 555, 104, FONTS['font_12'])

    # food
    if player.get_food() < 0:
        food = "%i" % player.get_food()
    else:
        food = "+%i" % player.get_food()
    GUI.bordered_text(DISPLAY, food, (0xff, 0xff, 0xff), (0x00, 0x00, 0x00), 555, 250, FONTS['font_12'])

    # rp_spent
#    research_costs = 50
#    if player['research'] > 0:
#	research_turns = (50 - player['research_progress']) / player['research']
#    else:
#	research_turns = "~"

    # research
    GUI.bordered_text(DISPLAY, "~%s turns" % player.get_research_turns_left(), (0xff, 0xff, 0xff), (0x00, 0x00, 0x00), 552, 386, FONTS['font_11_bold'])
    GUI.bordered_text(DISPLAY, "%i RP" % player.get_research(), (0xff, 0xff, 0xff), (0x00, 0x00, 0x00), 555, 400, FONTS['font_12_bold'])

    pygame.display.flip()

#    debug.debug_players(GAME)
#    debug.debug_stars(GAME)
#    debug.debug_colonies_population(GAME)
#    debug.debug_ships(GAME)

    return dynamic_buttons
# end func draw

##
#	RUN
##

def run(GAME):

    GAME['DATA'] = GAME['client'].fetch_game_data()

    for key in GAME:
        print("GAME[%s] ... %s" % (key, type(GAME[key])))

    for key in GAME['DATA']:
        print("GAME['DATA'][%s] ... %s" % (key, type(GAME['DATA'][key])))


    GUI = GAME['GUI']

#    print(dir(GAME['DATA']))
#    GAME['DATA'] = next_turn(GAME['client'])
#    print(GAME['DATA']['players'][0])

    triggers = [
            {'action': "game_menu",		'rect': pygame.Rect((255,   8), (50, 12))},
            {'action': "colonies_screen",	'rect': pygame.Rect(( 20, 431), (65, 38))},
            {'action': "leaders_screen",	'rect': pygame.Rect((315, 431), (65, 38))},
            {'action': "info_screen",		'rect': pygame.Rect((460, 431), (65, 38))},
            {'action': "research_screen",	'rect': pygame.Rect((547, 347), (64, 64))},
            {'action': "newTurn",		'rect': pygame.Rect((547, 444), (59, 19))},
            {'action': "planets_screen",        'rect': pygame.Rect((93, 431), (65, 38))}
        ] + draw(GAME)

    GUI.set_image('COLSUM', GUI.load_image('COLSUM.LBX', 0, 0, 'COLSUM.LBX', None))

    keys = {
        'KEYDOWN:99':		"colonies_screen",	# C
        'KEYDOWN:103':		"game_menu",		# G
        'KEYDOWN:105':		"info_screen",		# I
        'KEYDOWN:108':		"leaders_screen",	# L
        'KEYDOWN:116':		"newTurn"		# T
    }

    player		= GAME['DATA']['me']

    while True:

        if player.get_research_progress() == -1:
            action = "research_screen"
            player.set_research_progress(0)
        else:
            event = get_input.get_input(triggers)
            action = event['action']

        """
            Keyboard input:
                c = Colonies
                l = Leaders
                t = New Turn
        """
        if keys.has_key(action):
            action = keys[action]

        if (action == "QUIT"):
            quit_game(GAME)

        elif (action == "newTurn"):
#	    print("=> newTurn ... DATA.keys = %s" % GAME['DATA'].keys())
#            GAME['DATA'] =
            if GAME['client'].next_turn():
                print("# NEXT_TURN succesfully sent")
                while True:
                    NEW_DATA = GAME['client'].fetch_game_data()
                    if NEW_DATA:
                        GAME['DATA'] = NEW_DATA
                        draw(GAME)
                        break
                    else:
                        print("ERROR: received None from GameClient::next_turn()")
            else:
                print("! ERROR: NEXT_TURN sent failed?")
#	    print("=> newTurn ... result = %s" % result)

        elif (action == "colonies_screen"):
            colonies_screen.run(GAME)
            draw(GAME)

        elif (action == "leaders_screen"):
            leaders_screen.run(GAME)
            draw(GAME)

        elif (action == "info_screen"):
            info_screen.run(GAME)
            draw(GAME)

        elif (action == "planets_screen"):
            planets_screen.run(GAME)
            draw(GAME)

        elif (action == "research_screen"):
            research_screen.run(GAME)
            draw(GAME)

        elif (action[:12] == "systemDetail"):
            dialog_star_system.run(GAME, int(action[13:]))
            draw(GAME)

        elif (action == "game_menu"):
            game_menu.run(GAME)
            draw(GAME)

        else:
            print "UNKNONW ACTION: " + action

#  end func run


def quit_game(GAME):
    GAME['client'].logout()
    print
    print "@@@ quit_game"
    print "     turn: %i" % GAME['TURN']
    sys.exit(0)
