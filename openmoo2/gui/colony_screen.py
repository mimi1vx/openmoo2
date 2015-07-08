import pygame
import screen

from _game_constants import *

import networking
import gui
import dictionary

import text_box

class ColonyScreen(screen.Screen):

    def __init__(self):
        screen.Screen.__init__(self)

    def open_colony(self, colony_id):
        self.__colony_id = colony_id
        self.__colony = networking.Client.get_colony(colony_id)

        self.__planet_id = self.__colony.get_planet_id()
        self.__planet = networking.Client.get_planet(self.__planet_id)

        self.__star_id	= self.__planet.get_star()
        self.__star = networking.Client.get_star(self.__star_id)

    def reset_triggers_list(self):
        screen.Screen.reset_triggers_list(self)
        self.add_trigger({'action': "ESCAPE",    	'rect': pygame.Rect((556, 459), ( 72, 20))})
        self.add_trigger({'action': "leaders",   	'rect': pygame.Rect((556, 427), ( 72, 20))})
        self.add_trigger({'action': "buy",       	'rect': pygame.Rect((590, 123), ( 37, 22))})
        self.add_trigger({'action': "summary",	'summary': "morale", 'rect': pygame.Rect((309,  31), (202, 25))})
        self.add_trigger({'action': "summary",	'summary': "bc", 'rect': pygame.Rect((127,  31), (177, 25))})
        self.add_trigger({'action': "summary",	'summary': "food", 'rect': pygame.Rect((127,  61), (177, 25))})
        self.add_trigger({'action': "summary",	'summary': "industry", 'rect': pygame.Rect((127,  91), (177, 25))})
        self.add_trigger({'action': "summary",	'summary': "research", 'rect': pygame.Rect((127, 121), (177, 25))})

    def draw(self):
        DISPLAY = gui.GUI.get_display()
        DICTIONARY = dictionary.get_dictionary()
        PLAYERS = networking.Client.list_players()
        PLANETS = networking.Client.list_planets()
        
        font2 = gui.GUI.get_font('font2')
        font3 = gui.GUI.get_font('font3')
        font5 = gui.GUI.get_font('font5')

        star = self.__star
        planet = self.__planet
        colony = self.__colony

        DISPLAY.blit(self.get_image('background', 'starfield'), (0, 0))
        DISPLAY.blit(gui.GUI.get_planet_background(planet.get_terrain(), planet.get_picture()), (0, 0))
        DISPLAY.blit(self.get_image('colony_screen', 'panel'), (0, 0))

        colony_id = colony.get_id()

        self.reset_triggers_list()
        self.add_trigger({'action': "screen", 'screen': "colony_production", 'colony_id': colony_id, 'rect': pygame.Rect((519, 123), ( 61, 22))})

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
        gui.GUI.repeat_draw(DISPLAY, 340, 35, self.get_image('morale_icon', 'good'), colony.morale() // 10, 30, 7, 155)

        x = 10 + gui.GUI.repeat_draw(DISPLAY, 128, 64, self.get_image('production_10food'), colony.get_food() // 10, 20, 6, 98)
        gui.GUI.repeat_draw(DISPLAY, x, 64, self.get_image('production_1food'), colony.get_food() % 10, 20, 6, 98)

        # industry icons
        number = (colony.get_industry() // 10) + (colony.get_industry() % 10)
        xx = min(int(round(160 / max(1, number))), 20)
        print "### colony_screen::draw ... industry icons ... number = %i, xx = %i" % (number, xx)
        x =  gui.GUI.repeat_draw(DISPLAY, 128, 94, self.get_image('production_10industry'), colony.get_industry() // 10, xx, 99, 162)
        gui.GUI.repeat_draw(DISPLAY, x, 94, self.get_image('production_1industry'), colony.get_industry() % 10, xx, 99, 162)

        # research icons

        number = (colony.get_research() // 10) + (colony.get_research() % 10)
        xx = min(int(round(160 / max(1, number))), 20)
        print "### colony_screen::draw ... research icons ... number = %i, xx = %i" % (number, xx)
        x =  gui.GUI.repeat_draw(DISPLAY, 128, 124,self.get_image('production_10research'), colony.get_research() // 10, xx, 99, 162)
        gui.GUI.repeat_draw(DISPLAY, x, 124, self.get_image('production_1research'), colony.get_research() % 10, xx, 99, 162)

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

    def process_trigger(self, trigger):

        colony = networking.Client.get_colony(self.__colony_id)

        planet_id = colony.get_planet_id()
        planet = networking.Client.get_planet(planet_id)

        star_id	= planet.get_star()
        star = networking.Client.get_star(star_id)

        action = trigger['action']
        print("@ colony_screen::process_trigger()")

        if trigger['action'] == "summary":
            summary = trigger['summary']

            if summary == "morale":
                text_box.Screen.set_title("Morale Summary")
                text_box.Screen.set_content(colony.print_morale_summary())

            elif summary == "bc":
                text_box.Screen.set_title("BC Summary")
                text_box.Screen.set_content(colony.print_bc_summary())

            elif summary == "food":
                text_box.Screen.set_title("Food Summary")
                text_box.Screen.set_content(colony.print_food_summary())

            elif summary == "industry":
                text_box.Screen.set_title("Industry Summary")
                text_box.Screen.set_content(colony.print_industry_summary())

            elif summary == "research":
                text_box.Screen.set_title("Research Summary")
                text_box.Screen.set_content(colony.print_research_summary())

            gui.GUI.run_screen(text_box.Screen)
            self.redraw_flip()

        print("/ colony_screen::process_trigger()")



Screen = ColonyScreen()