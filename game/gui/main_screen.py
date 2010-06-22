import pygame
from screen import Screen

from game import stardate

class MainScreen(Screen):

    def __init__(self, ui):
        Screen.__init__(self, ui)

    def reset_triggers_list(self):
        Screen.reset_triggers_list(self)
        self.add_trigger({'action': "game_menu",        'rect': pygame.Rect((255,   8), (50, 12))})
        self.add_trigger({'action': "colonies_screen",	'rect': pygame.Rect(( 20, 431), (65, 38))})
        self.add_trigger({'action': "leaders_screen",	'rect': pygame.Rect((315, 431), (65, 38))})
        self.add_trigger({'action': "info_screen",	'rect': pygame.Rect((460, 431), (65, 38))})
        self.add_trigger({'action': "research_screen",	'rect': pygame.Rect((547, 347), (64, 66))})
        self.add_trigger({'action': "newTurn",		'rect': pygame.Rect((547, 444), (59, 19))})
        self.add_trigger({'action': "planets_screen",    'rect': pygame.Rect((93, 431), (65, 38))})

    def draw_stars(self):
        DISPLAY = self.get_display()

        GAME = self.__GAME
        DATA     = GAME['DATA']
        GALAXY   = DATA['galaxy']
        STARS    = DATA['stars']
        ME       = DATA['me']

        font4 = self.get_font('font4')

        WORMHOLE_COLOR = 0x242428
        map_x, map_y, map_width, map_height = 22, 21, 505, 400

        galaxy_width = GALAXY['width']
        galaxy_height = GALAXY['height']

        # wormholes
        wormholes = {}
        for star_id, star in STARS.items():

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
                    pygame.draw.line(self.get_display(), WORMHOLE_COLOR, (x1, y1), (x2, y2), 1)

        # stars
        for star_id, star in STARS.items():

            star_class = star.get_class()
            star_size = 2 - star.get_size() + self.__zoom_level

            star_icon = self.get_image('star_icon', star_class, star_size)
            pic_width, pic_height = star_icon.get_size()

            x = map_x + ((star.get_x() * map_width) / galaxy_width)
            y = map_y + ((star.get_y() * map_height) / galaxy_height)

            # icon
            if star_class < 7:
                xx = pic_width / 2
                yy = pic_height / 2
                self.add_trigger({'action': "show_star_system", 'star_id': star.get_id(), 'rect': pygame.Rect((x - xx, y - yy), (pic_width, pic_height))})
                DISPLAY.blit(star_icon, (x - xx, y - yy))

            # name
            yy = pic_height / 2
            if star.visited():
                starname = font4.render(star.get_name(), [0x0, 0x101018, 0x6c6c74], 1)
                DISPLAY.blit(starname, (x - (starname.get_width() / 2), y + yy - 2))

    def draw(self):
        DISPLAY = self.get_display()

        GAME = self.__GAME
        DATA     = GAME['DATA']
        GALAXY   = DATA['galaxy']
        STARS    = DATA['stars']
        ME       = DATA['me']

        font3 = self.get_font('font3')
        font4 = self.get_font('font4')

        self.reset_triggers_list()
        DISPLAY.blit(self.get_image('background', 'starfield'), (0, 0))
        DISPLAY.blit(self.get_image('main_screen', 'panel'), (0, 0))
        self.draw_stars()

        # stardate
        stardate_palette = [0x0, 0x7c7c84, 0xbcbcc4]
        font3.write_text(DISPLAY, 561, 29, stardate(GALAXY['stardate']), stardate_palette, 2)

        # research
        research_palette = [0x0, 0x7c7c84, 0xbcbcc4]
        font4.write_text(DISPLAY, 552, 380, "~%s turns" % ME.get_research_turns_left(), research_palette, 2)
        font4.write_text(DISPLAY, 552, 400, "%i RP" % ME.get_research(), research_palette, 2)

        self.flip()

    def run(self, GAME):
        GAME['DATA'] = GAME['client'].fetch_game_data()

        if GAME['DATA'] is None:
            self.log_error("no data received in main_screen::run()")
            return

        self.__GAME     = GAME
        DATA     = GAME['DATA']
        GALAXY   = DATA['galaxy']
#        STARS    = DATA['stars']
#        ME       = DATA['me']
#        GAME['data']     = GAME['DATA']
#        GALAXY   = GAME['data']['galaxy']
#        STARS    = GAME['data']['stars']
#        ME   = GAME['data']['me']

        galaxy_size_factor = GALAXY['size_factor']

        # set starting zoom factor
        if galaxy_size_factor < 6:
            self.__zoom_level = 4
        elif galaxy_size_factor < 11:
            self.__zoom_level = 3
        elif galaxy_size_factor < 16:
            self.__zoom_level = 2
        elif galaxy_size_factor < 21:
            self.__zoom_level = 1
        else:
            self.__zoom_level = 0

        self.draw()

        while True:
            event = self.get_event()
            if event:
                action = event['action']

                if action == "QUIT":
                    break

		elif action == "newTurn":
		#           print("=> newTurn ... DATA.keys = %s" % GAME['DATA'].keys()) 
		#            GAME['DATA'] = 
		    if GAME['client'].next_turn():
			print("# NEXT_TURN succesfully sent")
			while True:
			    NEW_DATA = GAME['client'].fetch_game_data()
			    if NEW_DATA:
				GAME['DATA'] = NEW_DATA
#    				self.__GAME     = GAME
				self.draw()
				break
			    else:
				print("ERROR: received None from GameClient::next_turn()")
		    else:
			print("! ERROR: NEXT_TURN sent failed?")
		#           print("=> newTurn ... result = %s" % result)

                elif action == "research_screen":
                    self.get_screen('RESEARCH').run(GAME)
                    self.draw()

                elif action == "colonies_screen":
                    self.get_screen('COLONIES').run(GAME)
                    self.draw()

                elif action == "planets_screen":
                    self.get_screen('PLANETS').run(GAME)
                    self.draw()

                elif action == "leaders_screen":
                    self.get_screen('LEADERS').run(GAME)
                    self.draw()

                elif action == "info_screen":
                    self.get_screen('INFO').run(GAME)
                    self.draw()

                elif action == "show_star_system":
                    self.get_screen('STARSYSTEM').run(GAME, event['star_id'])
                    self.draw()

                elif action == "hover":
                    pass

                else:
                    self.log_info("gui_main_screen::run() ... UNKNONW event: %s" % event)
