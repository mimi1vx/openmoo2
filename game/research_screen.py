
__author__="peterman"
__date__ ="$Jan 7, 2009 8:44:49 PM$"

import pygame

import get_input

#from _technology import *


def list_techs_by_area(tech_table, research_area):
    techs = {}
    for tech_id in tech_table:
        if tech_table[tech_id]['area'] == research_area:
            techs[tech_id] = tech_table[tech_id]
    return techs
# end func list_techs_by_area

def debug_known_techs(known_techs, tech_table):
    print("")
    print("=== Known Technologies: ===")
    for tech_id in known_techs:
        print("technology = %i ... %s" % (tech_id, tech_table[tech_id]))
    print("=== /Known Technologies ===")
    print("")


##
#       DRAW
##
def draw(GAME, hover):
    DATA        = GAME['DATA']
    RULES       = DATA['rules']
    ME          = DATA['me']

    DISPLAY     = GAME['DISPLAY']
    FONTS       = GAME['FONTS']
    IMAGES      = GAME['IMAGES']
    DISPLAY.blit(IMAGES['RESEARCH_DIALOG']['panel'], (80, 0))

#    print("research_screen::draw() ... hover = %s" % hover)

    dynamic_triggers = []

    research_areas = ME.list_research_areas()

#    print research_areas
    
    for research in research_areas:
        research_index = RULES['research'][research]['index']
#        print "research_index = %i" % research_index
        first_tech_id = research_areas[research][0]
        first_tech = RULES['tech_table'][first_tech_id]
        area_id = first_tech['area']

        if ME.get_research_area() == area_id:
            color = (0x64, 0xd0, 0x00)
        else:
            color = (0x04, 0x78, 0x00)

#        print RULES['research_areas'][area_id]

        x = 95 + (226 * (research_index % 2))
        y = 50 + (105 * (research_index // 2))

        label = FONTS['font_14_bold'].render(RULES['research_areas'][area_id]['name'], 1, color)

        DISPLAY.blit(label, (x, y))

#        techs = list_techs_by_area(RULES['tech_table'], my_area)
        i = 0
        y += 16
        x += 10
        for tech_id in research_areas[research]:
#            print techs[tech_id]

            if (hover is not None) and (hover['action'] == "set_research") and (hover['tech_id'] == tech_id):
#                tech_color = (0x00, 0xff, 0x00)
                tech_color = (0xAA, 0xFF, 0xAA)
            else:
                tech_color = color

            label = FONTS['font_13_bold'].render(RULES['tech_table'][tech_id]['name'], 1, tech_color)
            l_w = label.get_width()
            l_h = label.get_height()

            yy = i * 16
            DISPLAY.blit(label, (x, y + yy))
            dynamic_triggers.append({'action': "set_research", 'tech_id': tech_id, 'rect': pygame.Rect((x, y + yy), (l_w, l_h))})
            i += 1

    pygame.display.flip()

    return dynamic_triggers
# end func draw

##
#       RUN
##
def run(GAME):

    DATA        = GAME['DATA']
    RULES       = DATA['rules']

    debug_known_techs(DATA['me'].get_known_techs(), RULES['tech_table'])

    hover = None

    triggers = [
        {'action': "ESCAPE",        'rect': pygame.Rect((0, 0), (79, 480))},
        {'action': "ESCAPE",        'rect': pygame.Rect((552, 0), (87, 480))}
    ] + draw(GAME, hover)


    while True:
        event = get_input.get_input(triggers)
        action = event['action']

        if action == "ESCAPE":
            return

        elif action == "set_research":
            tech_id = event['tech_id']
            print(">>> set_research ... tech_id = %i = %s" % (tech_id, RULES['tech_table'][tech_id]['name']))
            GAME['DATA']['me'].print_research_debug()
            GAME['DATA'] = GAME['client'].set_research(tech_id)
            GAME['DATA']['me'].print_research_debug()
            return


        elif action == "help":
            print(">>> help ... help = %s" % (event['help']))

        elif action == "hover":
#            print(">>> HOVER ... hover = %s" % (event['hover']))
            if hover != event['hover']:
                hover = event['hover']
                triggers = [
                    {'action': "ESCAPE",        'rect': pygame.Rect((0, 0), (79, 480))},
                    {'action': "ESCAPE",        'rect': pygame.Rect((552, 0), (87, 480))}
                ] + draw(GAME, hover)

        else:
            print "UNKNONW ACTION: " + action
    

