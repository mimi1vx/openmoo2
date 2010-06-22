import pygame

from _game_constants import *

from screen import Screen

from _buildings import *

def list_available_buildings(rules_buildings, colony_obj, known_techs):
    replaced_buildings = []
    for b_id in colony_obj.list_buildings():
        if rules_buildings[b_id].has_key("replaces"):
            print rules_buildings[b_id]['replaces']
            for rep_b_id in rules_buildings[b_id]['replaces']:
                replaced_buildings.append(rep_b_id)

    available_buildings = {}
    for b_id in rules_buildings:
        b_rec = rules_buildings[b_id]
        if b_rec['tech']:
            # knows required technology and not built
            if (b_rec['tech'] in known_techs) and (not colony_obj.has_building(b_id)) and (not b_id in replaced_buildings):
                available_buildings[b_id] = b_rec
    return available_buildings
# end func list_available_buildings

class ColonyBuildScreen(Screen):

    def __init__(self, ui):
        Screen.__init__(self, ui)

    def reset_triggers_list(self):
        Screen.reset_triggers_list(self)
        self.add_trigger({'action': "ESCAPE",        'rect': pygame.Rect((496, 448), (56, 16))})

    def draw(self, star, planet, colony):
        GAME = self.__GAME
        DISPLAY     = self.get_display()
#        IMAGES      = GAME['IMAGES']
#        PALETTES	= GAME['PALETTES']
#        FONTS       = GAME['FONTS']

        DATA        = GAME['DATA']
        RULES       = DATA['rules']
        PROTOTYPES  = DATA['prototypes']
        ME          = DATA['me']

        font3 = self.get_font3()

        buildings_palette = [0x0, 0x440c00, 0xac542c]

        DISPLAY.blit(self.get_image('background', 'starfield'), (0, 0))
#        colony_screen.draw_planet_background(GUI, DISPLAY, IMAGES, PALETTES, planet.get_terrain(), planet.get_picture())
        DISPLAY.blit(self.get_ui().get_planet_background(planet.get_terrain(), planet.get_picture()), (0, 0))

        shadow = pygame.Surface((640, 480))

    #    shadow.fill((0, 0, 0))
    #    shadow.fill((8, 8, 20))
        shadow.fill((28, 32, 44))
        shadow.set_alpha(180)
        DISPLAY.blit(shadow, (0, 0))

    #    c1 = (0, 0, 0, 128)
    #    c1 = (8, 8, 20, 128)
        c1 = (28, 32, 44, 128)

        for y in range(0, 480, 2):
            pygame.draw.line(DISPLAY, c1, (0, y), (639, y), 1)

    #    for x in range(0, 640, 2):
    #        pygame.draw.line(DISPLAY, c1, (x, 0), (x, 479), 1)

#        DISPLAY.blit(IMAGES['COLONY_BUILD_SCREEN']['screen'], (0, 0))
        DISPLAY.blit(self.get_image('colony_build_screen', 'panel'), (0, 0))

    #    buildings = colony.list_buildings()
        print("")
        print("=== Available Buildings: ===")
        available_buildings = list_available_buildings(RULES['buildings'], colony, ME.get_known_techs())

        av_b_sorted = []
        for building_id, building in available_buildings.items():
            av_b_sorted.append("%s:%i" % (building['name'], building_id))
        av_b_sorted.sort()

        y = 20
#        for building_id, building in available_buildings.items():
	# limit listing to 25 items here, overflow causes crash on Solaris, Python 2.6.5, Pygame 1.8.1
        for bld in av_b_sorted[:25]:
            bld = bld.split(":")
            building_name = bld[0]
            building_id = int(bld[1])
            print(building_id, building_name)
            font3.write_text(DISPLAY, 13, y, building_name, buildings_palette, 2)
            y += 18
        print("=== /Available Buildings ===")
        print("")

        self.flip()
        return

        print("")
        print("=== Prototypes: ===")
        yy = 0
        for i in range(5):
            prototype = PROTOTYPES[i]
            print("")
            print(prototype)
            print("")
            label_surface = FONTS['font_14_bold'].render(prototype['name'], 1, (0xE4, 0x88, 0x20))
            yy += 19
            DISPLAY.blit(label_surface, (484, 110 + yy))
        print("=== /Prototypes ===")
        print("")



        build_queue = colony.build_queue()
        yy = 0
        print("")
        print("=== Build Queue: ===")
        for queue_item in build_queue:
            print(queue_item)
            build_id = queue_item['item']
            if build_id <  255:
                if build_id == 150:
                    label = PROTOTYPES[0]['name']
                elif build_id == 148:
                    label = PROTOTYPES[1]['name']
                elif build_id == 147:
                    label = PROTOTYPES[2]['name']
                elif build_id == 145:
                    label = PROTOTYPES[3]['name']
                elif build_id == 144:
                    label = PROTOTYPES[4]['name']
                else:
                    label = BUILDINGS[build_id]['name']

                label_surface = FONTS['font_12_bold'].render(label, 1, (0xE4, 0x88, 0x20))
                xx = label_surface.get_width() // 2
                DISPLAY.blit(label_surface, (208 + 126 - xx, 332 + yy))
                yy += 20
        print("=== /Build Queue: ===")
        print("")

        pygame.display.flip()



    # end func draw

    #
    #       RUN
    #
    def run(self, GAME, colony_id):
        self.__GAME = GAME

        DATA	= GAME['DATA']

        colony      = DATA['colonies'][colony_id]

        planet_id	= colony.get_planet_id()
        planet      = DATA['planets'][planet_id]

        star_id	= planet.get_star()
        star	= DATA['stars'][star_id]

        self.draw(star, planet, colony)

        while True:
            event = self.get_event()
            if event:
                action = event['action']

                if action == "ESCAPE":
                    return
