import pygame

import screen
import networking
import gui

from dictionary import greek_num

import main_screen

class StarsystemScreen(screen.Screen):

    __panel_moved = False
    __panel_x_min = 22
    __panel_x_max = 180
    __panel_y_min = 22
    __panel_y_max = 148

    __panel_x = 106
    __panel_y = 103

    def __init__(self):
        screen.Screen.__init__(self)

    def __check_panel_moved(self):
        """Returns True if panel's position has changed and resets the moved flag"""
        if self.__panel_moved:
            self.__panel_moved = False
            return True
        else:
            return False

    def open_star(self, star_id):
        """Stores the id of a star system which is going to be displayed on this screen"""
        self.__star_id = star_id

    def get_normalized_panel_pos(self, (x, y)):
        """Returns panel position within allowed ranges to prevent escaping the main window boundaries"""
        return (min(max(x, self.__panel_x_min), self.__panel_x_max), min(max(y, self.__panel_y_min), self.__panel_y_max))

    def prepare(self):
        """Copy the actual content of MainScreen, it is used on each redraw"""
        self.__BACKGROUND = gui.GUI.get_display().copy()

    def draw_planet_info(self, text_rows):
        """Draws a semi-transparent minibox in the upper-left corner of the dialog window"""
        DISPLAY = gui.GUI.get_display()
        font3 = gui.GUI.get_font('font3')
        info_palette = [0x0, 0x181c40, 0x688cb0]
        info_x, info_y = self.get_normalized_panel_pos((self.__panel_x, self.__panel_y))
        info_x += 15
        info_y += 49
        rows = []
        width, height = 0, 6
        for text_line in text_rows:
            rows.append(font3.render(text_line, info_palette, 1))
            height += 13
            width = max(width, rows[-1].get_width())
        width += 8
        info_box = pygame.Surface((width, height))
        info_box.fill(0x000000)
        info_box.set_alpha(128)
#        pygame.draw.rect(info_box, 0x445c80, pygame.Rect((0, 0), (width - 1, height -1)), 2)
        DISPLAY.blit(info_box, (info_x, info_y))
        pygame.draw.rect(DISPLAY, 0x445c80, pygame.Rect((info_x, info_y), (width - 1, height -1)), 2)
        y = info_y + 5
        for row in rows:
            DISPLAY.blit(row, (info_x + 4, y))
            y += 13

    def draw(self):
        """Draws the background, starsystem dialog window, planets/asteroids orbit schemes, planets picturesand central star picture"""
        print("@ starsystem_screen.draw()")
        star_id = self.__star_id
        hover = self.get_hover()
        DISPLAY = gui.GUI.get_display()

        title_shadow_palette = [0x0, 0x181c40, 0x20284c, 0x20284c]
        title_palette = [0x0, 0x181c40, 0x506c90, 0x445c80]

        font5 = gui.GUI.get_font('font5')

        ME = networking.Client.get_me()

        star = networking.Client.get_star(star_id)

        self.reset_triggers_list()

        X, Y = self.get_normalized_panel_pos((self.__panel_x, self.__panel_y))

        self.add_trigger({'action': "ESCAPE", 'hover_id': "escape_button", 'rect': pygame.Rect((X + 264, Y + 239), (64, 19))})
        self.add_trigger({'action': "drag", 'drag_id': "window_title", 'rect': pygame.Rect((X + 14, Y + 12), (319, 26))})

        DISPLAY.blit(self.__BACKGROUND, (0, 0))

        # dialog window
        DISPLAY.blit(self.get_image('starsystem_map', 'panel'), (X, Y))

        # dialog title
        title = "Star System " + star.get_name()
        title_shadow = font5.render(title, title_shadow_palette, 2)
        title = font5.render(title, title_palette, 2)
        (tw, th) = title.get_size()

        DISPLAY.blit(title_shadow, (X + 174 - (tw / 2), Y + 20))
        DISPLAY.blit(title, (X + 173 - (tw / 2), Y + 19))

        if star.visited():

            DISPLAY.blit(self.get_image('starsystem_map', 'star', star.get_class()), (X + 156, Y + 120))

            show_info = None

            for i in range(5):
                planet_id = star.get_objects()[i]
                if planet_id != 0xffff:
                    planet = networking.Client.get_planet(planet_id)

                    # draw a planet/asteroid orbit scheme first
                    if planet.is_asteroid_belt():
                        if i == 0:
                            # FIXME: where are the asteroid belts for objects 1~4 ?
                            DISPLAY.blit(self.get_image('starsystem_map', 'asteroids', i), (X + 29, Y + 59))
                    elif planet.is_planet() or planet.is_gas_giant():
                        DISPLAY.blit(self.get_image('starsystem_map', 'orbit', i), (X + 29, Y + 59))

                    x = X + 200 + (25 * i) + (5 - planet.get_size())
                    y = Y + 121 + (5 - planet.get_size())
                    print("    hover = %s" % str(hover))
                    hover_id = "planet_%i" % planet_id
                    print("    hover_id = %s" % hover_id)

                    planet_size = planet.get_size()

                    planet_info = []

                    if planet.is_gas_giant():
                        planet_image = self.get_image('starsystem_map', 'gas_giant', planet_size)
                        w, h = planet_image.get_size()
                        w -= (10 - planet_size)
                        h -= (10 - planet_size)
                        planet_rect = pygame.Rect((x, y), (w, h))
                        DISPLAY.blit(planet_image, (x, y))
                        self.add_trigger({'action': "gas_giant", 'planet_id': planet_id, 'hover_id': hover_id, 'rect': planet_rect})
#                        if hover and hover['hover_id'] == hover_id:
                        planet_info.append("Gas Giant (uninhabitable)")

                    elif planet.is_planet():
                        planet_image = self.get_image('starsystem_map', 'planet', planet.get_terrain(), planet_size)
                        w, h = planet_image.get_size()
                        w -= (10 - planet_size)
                        h -= (10 - planet_size)
                        planet_rect = pygame.Rect((x, y), (w, h))

                        DISPLAY.blit(planet_image, (x, y))

                        planet_info.append("%s %s" % (star.get_name(), greek_num(i)))
                        planet_info.append("%s, %s" % (planet.size_text(), planet.terrain_text()))

                        colony_id = planet.get_colony_id()

                        if colony_id < 0xffff:
                            colony = networking.Client.get_colony(colony_id)
                            player = networking.Client.get_player(colony.get_owner())

                            if colony.is_owned_by(ME.get_id()) and colony.is_colony():
                                self.add_trigger({'action': "screen", 'screen': "colony", 'colony_id': colony_id, 'hover_id': hover_id, 'rect': planet_rect})
                                planet_info.append("%i / %i pop" % (colony.get_population(), colony.max_population()))
                            else:
                                self.add_trigger({'action': "enemy_colony", 'hover_id': hover_id, 'rect': planet_rect})
                                planet_info.append("??? enemy pop")
                                    
                            if colony.is_outpost():
                                DISPLAY.blit(self.get_image('starsystem_map', 'outpost_mark', player.get_color()), (x - 6, y))
                            else:
                                DISPLAY.blit(self.get_image('starsystem_map', 'colony_mark', player.get_color()), (x - 6, y))

                        else:
                            self.add_trigger({'action': "planet", 'planet_id': planet_id, 'hover_id': hover_id, 'rect': planet_rect})
                            planet_info.append("%i max pop" % planet.get_max_population())

                        planet_info.append("%s" % (planet.minerals_text()))

                        # set the info-box content if hover machtes
                    if hover and hover['hover_id'] == hover_id:
                        show_info = planet_info

            # finaly render the on-hover info-box so it's not over-drawed by a planet otbit schemes
            if show_info:
                self.draw_planet_info(show_info)

    def animate(self):
	"""Redraws the draggable panel"""
        if self.hover_changed() or self.__check_panel_moved():
            self.redraw_noflip()

    def on_mousedrag(self, drag_item, (mouse_x, mouse_y), (rel_x, rel_y)):
        """Updates the panel position and sets the moved flag"""
        self.__panel_x += rel_x
	self.__panel_y += rel_y
        self.__panel_moved = True

    def on_mousedrop(self, drag_item, (mouse_x, mouse_y)):
	"""Just reset the panel position so next time drag will not be affected by out-of border position"""
        self.__panel_x, self.__panel_y = self.get_normalized_panel_pos((self.__panel_x, self.__panel_y))



Screen = StarsystemScreen()