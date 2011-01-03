import pygame

import screen
import networking
import gui

from game import stardate

ship_tracks_bitmaps = (
    [0x001400, 0x001400, 0x043804, 0x087008, 0x489038, 0x489038, 0x087008, 0x043804],
    [0x043804, 0x001400, 0x001400, 0x043804, 0x087008, 0x489038, 0x489038, 0x087008],
    [0x087008, 0x043804, 0x001400, 0x001400, 0x043804, 0x087008, 0x489038, 0x489038],
    [0x489038, 0x087008, 0x043804, 0x001400, 0x001400, 0x043804, 0x087008, 0x489038],
    [0x489038, 0x489038, 0x087008, 0x043804, 0x001400, 0x001400, 0x043804, 0x087008],
    [0x087008, 0x489038, 0x489038, 0x087008, 0x043804, 0x001400, 0x001400, 0x043804],
    [0x043804, 0x087008, 0x489038, 0x489038, 0x087008, 0x043804, 0x001400, 0x001400],
    [0x001400, 0x043804, 0x087008, 0x489038, 0x489038, 0x087008, 0x043804, 0x001400]
)

class MainScreen(screen.Screen):

    def __init__(self):
        screen.Screen.__init__(self)
        self.__map_x = 22
        self.__map_y = 21
        self.__map_width = 505
        self.__map_height = 400
	self.__tick = None

    def reset_triggers_list(self):
        screen.Screen.reset_triggers_list(self)
        self.add_trigger({'action': "screen", 'screen': "game_menu",        'rect': pygame.Rect((255,   8), (50, 12))})
        self.add_trigger({'action': "screen", 'screen': "colonies",	'rect': pygame.Rect(( 20, 431), (65, 38)), 'key': 99}) # C key
        self.add_trigger({'action': "screen", 'screen': "leaders",	'rect': pygame.Rect((315, 431), (65, 38)), 'key': 108}) # L key
        self.add_trigger({'action': "screen", 'screen': "info",	'rect': pygame.Rect((460, 431), (65, 38)), 'key': 105}) # I key
        self.add_trigger({'action': "screen", 'screen': "research",	'rect': pygame.Rect((547, 347), (64, 66))})
        self.add_trigger({'action': "newTurn",		'rect': pygame.Rect((547, 444), (59, 19))})
        self.add_trigger({'action': "screen", 'screen': "planets",    'rect': pygame.Rect((93, 431), (65, 38)), 'key': 112}) # P key
        self.add_trigger({'action': "screen", 'screen': "fleets",    'rect': pygame.Rect((160, 431), (65, 38)), 'key': 102}) # F key

    def get_pos(self, (x, y)):
        pos_x = self.__map_x + ((x * self.__map_width) / self.__galaxy_width)
        pos_y = self.__map_y + ((y * self.__map_height) / self.__galaxy_height)
        return (pos_x, pos_y)

    def clear_map_items(self):
        self.__map_items = {
            'wormholes': [],
            'ship_tracks': [],
            'stars': [],
            'ships': []
        }

    def register_map_item(self, group_key, img, (x1, y1), (x2, y2) = (-1, -1)):
        self.__map_items[group_key].append({'img': img, 'pos1': (x1, y1), 'pos2': (x2, y2)})

    def prepare_stars(self):
        STARS    = networking.Client.list_stars()

        font4 = gui.GUI.get_font('font4')

        map_x, map_y, map_width, map_height = 22, 21, 505, 400

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
                         x1, y1 = self.get_pos(star.get_coords())
                         x2, y2 = self.get_pos(star2.get_coords())
                         wormholes[key] = True
                    self.register_map_item('wormholes', None, (x1, y1), (x2, y2))

        # stars
        for star_id, star in STARS.items():

            star_class = star.get_class()
            star_size = 2 - star.get_size() + self.__zoom_level

            star_icon = self.get_image('star_icon', star_class, star_size)
            pic_width, pic_height = star_icon.get_size()

            x, y = self.get_pos(star.get_coords())

            # icon
            if star_class < 7:
                xx = pic_width / 2
                yy = pic_height / 2
                self.add_trigger({'action': "screen", 'screen': "starsystem", 'star_id': star.get_id(), 'rect': pygame.Rect((x - xx + 3, y - yy + 3), (pic_width - 6, pic_height - 6))})
                self.register_map_item('stars', star_icon, (x - xx, y - yy))

            # name
            yy = pic_height / 2
            if star.visited():
                starname = font4.render(star.get_name(), [0x0, 0x101018, 0x6c6c74], 1)
                self.register_map_item('stars', starname, (x - (starname.get_width() / 2), y + yy - 2))

    def prepare_ships(self):

        map_x, map_y, map_width, map_height = 22, 21, 505, 400

        PLAYERS = networking.Client.list_players()
        STARS    = networking.Client.list_stars()
        SHIPS = networking.Client.list_ship_ids()
        STARS_BY_COORDS = networking.Client.list_stars_by_coords()

        for ship_id in SHIPS:
            draw = False
            track = False
            ship = SHIPS[ship_id]

            ship_icon_x, ship_icon_y = self.get_pos(ship.get_coords())

            ship_icon_size = self.__zoom_level
            ship_destination = ship.get_destination()
            if ship.get_owner() < 8:
                ship_icon_color = PLAYERS[ship.get_owner()].get_color()
            else:
                ship_icon_color = ship.get_owner()
            ship_icon = self.get_image('main_screen', 'ship_icon', ship_icon_color, ship_icon_size)

#            ship.print_debug(PLAYERS[ship.get_owner()], STARS)

            if ship.is_orbiting():
                draw = True
                star_class = STARS[ship_destination].get_class()
                star_pic_size = 2 - STARS[ship_destination].get_size() + self.__zoom_level
                star_icon = self.get_image('star_icon', star_class, star_pic_size)
                spic_w, spic_h = star_icon.get_size()
                ship_icon_x += (spic_w / 3) + 2 - self.__zoom_level
                ship_icon_y -= (spic_h / 2)
            elif ship.is_travelling():
                draw = True
                track = True
                ship_w, ship_h = ship_icon.get_size()
                ship_icon_x -= (ship_w / 2) - 4
                ship_icon_y -= (ship_h / 2) - 2
            elif ship.is_launching():
                draw = True
                track = True
                k = "%i:%i" % (ship.get_x(), ship.get_y())
                star_class = STARS_BY_COORDS[k].get_class()
                star_pic_size = 2 - STARS_BY_COORDS[k].get_size() + self.__zoom_level
                star_icon = self.get_image('star_icon', star_class, star_pic_size)
                spic_w, spic_h = star_icon.get_size()
                ship_icon_x -= (spic_w / 2) + 8
                ship_icon_y -= (spic_h / 2) + 1
            if draw:
                if track:
                    ship_xx = ship_icon.get_width() / 2
                    ship_yy = ship_icon.get_height() / 2
                    star_x, star_y = self.get_pos(STARS[ship_destination].get_coords())
                    self.register_map_item('ship_tracks', None, (ship_icon_x + ship_xx, ship_icon_y + ship_yy), (star_x, star_y))
                self.register_map_item('ships', ship_icon, (ship_icon_x, ship_icon_y))

    def draw(self):
        DISPLAY = gui.GUI.get_display()

        ME       = networking.Client.get_me()

        font3 = gui.GUI.get_font('font3')
        font4 = gui.GUI.get_font('font4')

        self.reset_triggers_list()
        gui.GUI.draw_image_by_key('background.starfield', (0, 0))
        gui.GUI.draw_image_by_key('main_screen.panel', (0, 0))

        # main screen draws a lot of objects in "layers" so map images are prepared first and draw in groups after that
        self.clear_map_items()
        self.prepare_ships()
        self.prepare_stars()

        # stardate
        stardate_palette = [0x0, 0x7c7c84, 0xbcbcc4]
        font3.write_text(DISPLAY, 561, 29, stardate(networking.Client.get_stardate()), stardate_palette, 2)

        # research
        research_palette = [0x0, 0x7c7c84, 0xbcbcc4]
        font4.write_text(DISPLAY, 552, 380, "~%s turns" % ME.get_research_turns_left(), research_palette, 2)
        font4.write_text(DISPLAY, 552, 400, "%i RP" % ME.get_research(), research_palette, 2)

    def animate(self):
        ts = self.get_timestamp(20)
	tick = ts % 8
	if self.__tick != tick:
#            print("@ main_screen.animate() ... TICK")
	    self.__tick = tick
            DISPLAY = gui.GUI.get_display()
            for wormhole in self.__map_items['wormholes']:
                gui.GUI.draw_line(wormhole['pos1'], wormhole['pos2'], [0x444444])

            for ship_track in self.__map_items['ship_tracks']:
                gui.GUI.draw_line(ship_track['pos1'], ship_track['pos2'], ship_tracks_bitmaps[tick])

            for star in self.__map_items['stars']:
            	gui.GUI.draw_image(star['img'], star['pos1'])

            for ship in self.__map_items['ships']:
                gui.GUI.draw_image(ship['img'], ship['pos1'])

            return True

        else:
            return False

    def start(self):
        GALAXY = networking.Client.get_galaxy()

        galaxy_size_factor = GALAXY['size_factor']

        self.__galaxy_width = GALAXY['width']
        self.__galaxy_height = GALAXY['height']

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

    def process_trigger(self, trigger):
        pass


Screen = MainScreen()