import pygame
from screen import Screen

from game import stardate

from _game_constants import *

class ColonyScreen(Screen):

    def __init__(self, ui):
        Screen.__init__(self, ui)

    def reset_triggers_list(self):
        Screen.reset_triggers_list(self)
        self.add_trigger({'action': "ESCAPE",    	'rect': pygame.Rect((556, 459), ( 72, 20))})
        self.add_trigger({'action': "leaders",   	'rect': pygame.Rect((556, 427), ( 72, 20))})
        self.add_trigger({'action': "buy",       	'rect': pygame.Rect((590, 123), ( 37, 22))})
        self.add_trigger({'action': "morale_summary",	'rect': pygame.Rect((309,  31), (202, 25))})
        self.add_trigger({'action': "bc_summary",	'rect': pygame.Rect((127,  31), (177, 25))})
        self.add_trigger({'action': "food_summary",	'rect': pygame.Rect((127,  61), (177, 25))})
        self.add_trigger({'action': "industry_summary",	'rect': pygame.Rect((127,  91), (177, 25))})
        self.add_trigger({'action': "research_summary",	'rect': pygame.Rect((127, 121), (177, 25))})

    def draw(self, star, planet, colony):
        DISPLAY         = self.get_display()
        GAME            = self.__GAME
        DICTIONARY	= GAME['DICTIONARY']
        PLAYERS         = GAME['DATA']['players']
        PLANETS         = GAME['DATA']['planets']
        
        font2 = self.get_font('font2')
        font3 = self.get_font('font3')
        font5 = self.get_font('font5')

        DISPLAY.blit(self.get_image('background', 'starfield'), (0, 0))
        DISPLAY.blit(self.get_ui().get_planet_background(planet.get_terrain(), planet.get_picture()), (0, 0))
        DISPLAY.blit(self.get_image('colony_screen', 'panel'), (0, 0))

        colony_id = colony.get_id()

        self.reset_triggers_list()
        self.add_trigger({'action': "change_build", 'colony_id': colony_id, 'rect': pygame.Rect((519, 123), ( 61, 22))})

        schemes_font_palette = [0x0, 0x141420, 0x6c688c]

        for i in range(5):
            object_id = star.get_objects()[i]
            if object_id != 0xFFFF:
                object = PLANETS[object_id]
                print "type: %i" % object.get_type()

                if object.is_asteroid_belt():
                    x = 6
                    y = 22 + (24 * i)
                    DISPLAY.blit(self.get_image('colony_screen', 'asteroids_scheme'), (x, y))
                    font2.write_text(DISPLAY, x + 29, y + 9, "Asteroids", schemes_font_palette, 1)

                if object.is_gas_giant():
                    x = 11
                    y = 27 + (24 * i)
                    DISPLAY.blit(self.get_image('colony_screen', 'gasgiant_scheme'), (x, y))
                    font2.write_text(DISPLAY, x + 24, y + 4, "Gas Giant -", schemes_font_palette, 1)
                    font2.write_text(DISPLAY, x + 24, y + 15, "uninhabitable", schemes_font_palette, 1)

                elif object.is_planet():
                    terrain = object.get_terrain()
                    size = object.get_size()
                    x = 10 + [6, 4, 3, 1, 0][size]
                    y = 26 + (24 * i) + [6, 4, 2, 1, 0][size]
#                    DISPLAY.blit(self.get_ui().get_planet_scheme(terrain, size), (x, y))
                    DISPLAY.blit(self.get_image('planet_scheme', terrain, size), (x, y))

            DISPLAY.blit(self.get_image('colony_screen', 'scheme_arrow'), (6,  31 + (24 * i)))

        title = "%s of %s" % (DICTIONARY['COLONY_ASSIGNMENT'][colony.assignment], colony.get_name())

        title_palette = [0x0, 0x141420, 0x6c688c, 0x605c80]

        title_surface = font5.render(title, title_palette, 2 )
        (tw, th) = title_surface.get_size()

        DISPLAY.blit(title_surface, (320 - (tw / 2), 1))

    #    total_population = (1000 * colony['population']) + colony['pop_raised']
    #    print
    #    print "	Colony:		%s" % colony.name
    #    print "	Population:	%i (+%i)" % (total_population, colony['pop_grow'])
    #    print "	Industry:	%i" % colony.industry()
    #    print "	Research:	%i" % colony.research()
    #    print "	Food (result):	%i (%i)" % (colony.food(), colony.food() - colony.population)
    #    print "	Colonists:"

        player_government_id = PLAYERS[colony.get_owner()].get_racepick_item('goverment')

        DISPLAY.blit(self.get_image('government', 'icon', player_government_id), (310, 32))

        # TODO: implement negative morale
        self.repeat_draw(DISPLAY, 340, 35, self.get_image('morale_icon', 'good'), colony.morale() // 10, 30, 7, 155)

        x = 10 + self.repeat_draw(DISPLAY, 128, 64, self.get_image('production_10food'), colony.get_food() // 10, 20, 6, 98)
        self.repeat_draw(DISPLAY, x, 64, self.get_image('production_1food'), colony.get_food() % 10, 20, 6, 98)

        # industry icons
        number = (colony.get_industry() // 10) + (colony.get_industry() % 10)
        xx = min(int(round(160 / max(1, number))), 20)
        print "### colony_screen::draw ... industry icons ... number = %i, xx = %i" % (number, xx)
        x =  self.repeat_draw(DISPLAY, 128, 94, self.get_image('production_10industry'), colony.get_industry() // 10, xx, 99, 162)
        self.repeat_draw(DISPLAY, x, 94, self.get_image('production_1industry'), colony.get_industry() % 10, xx, 99, 162)

        # research icons

        number = (colony.get_research() // 10) + (colony.get_research() % 10)
        xx = min(int(round(160 / max(1, number))), 20)
        print "### colony_screen::draw ... research icons ... number = %i, xx = %i" % (number, xx)
        x =  self.repeat_draw(DISPLAY, 128, 124,self.get_image('production_10research'), colony.get_research() // 10, xx, 99, 162)
        self.repeat_draw(DISPLAY, x, 124, self.get_image('production_1research'), colony.get_research() % 10, xx, 99, 162)

        for t in (FARMER, WORKER, SCIENTIST):
            c = len(colony.colonists[t])
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
                race = Colonist['race']
                picture = PLAYERS[race].get_picture()
                x = 310 + xx * i
#                DISPLAY.blit(self.get_race_icon(picture, icon), (x, y))
                DISPLAY.blit(self.get_image('race_icon', picture, icon), (x, y))
                if i == (c - 1):
                    xx = 28	# enlarge the Rect of last icon (no other icon is drawn over it...)
                self.add_trigger({'action': "pick-colonist:%.2x:%i" % (t, (c - i)),    'rect': pygame.Rect((x, y), (xx, 28))})

        x = 0
        for i in range(colony.marines):
#            DISPLAY.blit(self.get_race_icon(picture, 0x07), (x, 450))
            DISPLAY.blit(self.get_image('race_icon', picture, 0x07), (x, 450))
            x += 30

        # TODO: count in all races not just owner!
        total_population = (1000 * colony.total_population()) + sum(colony.pop_raised())
        pop_s = "Pop %i,%.3i k (+%i)" % ((total_population // 1000), (total_population % 1000), sum(colony.pop_grow()))

        population_palette = [0x0, 0x141420, 0x6c688c]

        population = font3.render(pop_s, population_palette, 2)

        (tw, th) = population.get_size()

        DISPLAY.blit(population, (529, 3))

        pygame.display.flip()

    # end func draw

        self.flip()

    def run(self, GAME, colony_id):
    #    draw(GAME)
        self.__GAME = GAME
        DATA	= GAME['DATA']


        print
        print "@@@ colony_screen @@@"

        colony      = DATA['colonies'][colony_id]

        planet_id	= colony.get_planet_id()
        planet      = DATA['planets'][planet_id]

        star_id	= planet.get_star()
        star	= DATA['stars'][star_id]

        for build_item in colony.get_build_queue():
            print "colony_screen::run() ... colony.build_queue[] = %s" % build_item

        self.draw(star, planet, colony)

        while True:
            event = self.get_event()
            if event:
                action = event['action']
                if action == "ESCAPE"):
                    return
           
                elif action == "morale_summary":
                    summary = colony.print_morale_summary();
                    GUI.draw_textbox(summary, 135, 190,'Morale Summary')
                    triggers2 = draw(GAME, star, planet, colony)

            
                elif action == "bc_summary":
                    summary = colony.print_bc_summary();
                    GUI.draw_textbox( summary, 135, 190, 'BC Summary')
                    triggers2 = draw(GAME, star, planet, colony)

                elif action == "food_summary":
                    summary = colony.print_food_summary();
                    GUI.draw_textbox(summary, 135, 190, 'Food Summary')
                    triggers2 = draw(GAME, star, planet, colony)

                elif action == "industry_summary":
                    summary = colony.print_industry_summary();
                    GUI.draw_textbox(summary, 135, 190, 'Industry Summary')
                    triggers2 = draw(GAME, star, planet, colony)

                elif action == "research_summary":
                    summary = colony.print_research_summary();
                    GUI.draw_textbox(summary, 135, 190, 'Research Summary')
                    triggers2 = draw(GAME, star, planet, colony)

                elif action == "change_build":
                    colony_build_screen.run(GAME, colony_id)
                    triggers2 = draw(GAME, star, planet, colony)

                else:
                    print "UNKNOWN ACTION: " + action

