import pygame

from screen import Screen

class PlanetsScreen(Screen):

    def get_planets_to_display(self, player_id):
        planets = []
        stars_i = self.__DATA['stars']
        stars = []
        for i_s in stars_i:
            stars.append(self.__DATA['stars'][i_s])
            
        for star in stars:
            if star.visited_by_player(player_id):
                objects = star.get_objects()
                for id in objects:
                    planet_id = id
                    if planet_id != 0xffff:
                        planet = self.__DATA['planets'][planet_id]
                        if planet.is_planet():
                            planets.append(planet)
        return planets

    def scroll_up(self, step = 1):
        self.viewport_top_planet -=step
        if self.viewport_top_planet < 0:
                self.viewport_top_planet =0
        self.draw()
        return

    def scroll_down(self, step = 1):
        self.viewport_top_planet +=step
        if self.viewport_top_planet not in range(self.planets_to_display - self.viewport_size):
            self.viewport_top_planet = self.planets_to_display - self.viewport_size
        self.draw()
        return

    def __init__(self, ui):
        Screen.__init__(self, ui)
        self.viewport_size = 8
        self.viewport_top_planet = 0
        self.planets_to_display = 0

    def reset_triggers_list(self):
        Screen.reset_triggers_list(self)

        #sort priority triggers
        self.add_trigger({'action': "PRIORITY_CLIMATE", 'rect': pygame.Rect((440, 200), ( 60, 25))})
        self.add_trigger({'action': "PRIORITY_CLIMATE", 'rect': pygame.Rect((500, 200), ( 70, 25))})
        self.add_trigger({'action': "PRIORITY_CLIMATE", 'rect': pygame.Rect((570, 200), ( 60, 25))})

        #list filtering triggers
        trigger_y_size = 23
        trigger_x_size = 185
        self.add_trigger({'action': "FILTER_NO_ENEMY_PRESENCE", 'rect': pygame.Rect((440, 265), ( trigger_x_size, trigger_y_size))})
        self.add_trigger({'action': "FILTER_NORMAL_GRAVITY", 'rect': pygame.Rect((440, 265+1*trigger_y_size), ( trigger_x_size, trigger_y_size))})
        self.add_trigger({'action': "FILTER_NON_HOSTILE_ENVIROMENT", 'rect': pygame.Rect((440, 265+2*trigger_y_size), ( trigger_x_size, trigger_y_size))})
        self.add_trigger({'action': "FILTER_MINERAL_ABUNDANCE", 'rect': pygame.Rect((440, 265+3*trigger_y_size), ( trigger_x_size, trigger_y_size))})
        self.add_trigger({'action': "FILTER_PLANETS_IN_RANGE", 'rect': pygame.Rect((440, 265+4*trigger_y_size), ( trigger_x_size, trigger_y_size))})

        #button triggers
        self.add_trigger({'action': "ESCAPE", 'rect': pygame.Rect((455, 445), ( 150, 20))})
        self.add_trigger({'action': "SEND_COLONY_SHIP", 'rect': pygame.Rect((455, 390), ( 150, 20))})
        self.add_trigger({'action': "SEND_OUTPOST_SHIP", 'rect': pygame.Rect((455, 415), ( 150, 20))})
        self.add_trigger({'action': "VIEWPORT_UP", 'rect': pygame.Rect((422, 15), ( 10, 20))})
        self.add_trigger({'action': "VIEWPORT_DOWN", 'rect': pygame.Rect((422, 447), ( 10, 20))})
        self.add_trigger({'action': "SCROLL_UP", 'rect': pygame.Rect((422, 35), ( 12, 205))})
        self.add_trigger({'action': "SCROLL_DOWN", 'rect': pygame.Rect((422, 240), ( 12, 205))})

        return
    def draw_planet_globe(self,planet,DISPLAY,screen_obj,x,y):
        planet_image = screen_obj.get_image('starsystem_map', 'planet', planet.get_terrain(), planet.get_size())
        w, h = planet_image.get_size()
        w -= (10 - planet.get_size())
        h -= (10 - planet.get_size())
        planet_rect = pygame.Rect((x, y), (w, h))
        DISPLAY.blit(planet_image, (x-w/2, y-h/2))
        return planet_rect


    def draw(self):

        DISPLAY     = self.get_display()
        title_shadow_palette = [0x0, 0x181c40, 0x20284c, 0x20284c]
        title_palette = [0x0, 0x181c40, 0x506c90, 0x445c80]
        viewport_font_palette = [0x0, 0x181c40, 0x688cb0]
        font2 = self.get_font('font2')
        font3 = self.get_font('font3')
        font5 = self.get_font('font5')

        DISPLAY.blit(self.get_image('planets_screen', 'panel'), (0, 0))
   
        planets = self.get_planets_to_display(self.ME.get_id())
        #TODO: sorting planets 
        self.planets_to_display = len(planets)
        ftd = self.viewport_top_planet
        #x positions, centered, for texts and imgs in viewport
        x_poss = [60,140,215,310,385]
        y_poss = 60  # + i*55 -estimate, centers of display windows
        if (ftd + self.viewport_size) > len(planets):
            ftd = len(planets)- self.viewport_size

        for i in range(self.viewport_size):
            ptd = planets[ftd+i]
            txts = []

            star_id= ptd.get_star()

            name_t = self.__DATA['stars'][star_id].get_name()
            terrain_t = ptd.terrain_text()
            minerals_t = ptd.minerals_text()
            size_t = ptd.size_text()
            gravity_t = ptd.gravity_text()

            planet_y_offset = -4
            #estimate, from MOO2 screenshots. Planets are not drawn centered
            
            self.draw_planet_globe(ptd,DISPLAY, self, x_poss[0] , y_poss+55*i + planet_y_offset)

            offset_y = -5
            txts.append([font3.render(name_t, viewport_font_palette, 1),offset_y])
            txts.append([font3.render(terrain_t, viewport_font_palette, 1),offset_y])
            txts.append([font3.render(gravity_t, viewport_font_palette, 1),0])
            txts.append([font3.render(minerals_t, viewport_font_palette, 1),offset_y])
            txts.append([font3.render(size_t, viewport_font_palette, 1),offset_y])

            #TODO: get industry, population sizes and food prod data
            j=0
            for txt in txts:
                (tw, th) = txt[0].get_size()
                DISPLAY.blit(txt[0], (x_poss[j]-tw/2,y_poss+55*i+txt[1]-th/2))
                j+=1

        self.flip()

    def run(self, GAME):
        self.__GAME = GAME
        self.__DATA = GAME['DATA']
        self.ME = GAME['DATA']['me']
        
        self.draw()

        while True:
            event = self.get_event()
            if event:
                action = event['action']
                if action == "ESCAPE":
                    return
                if action == "VIEWPORT_UP":
                    self.scroll_up()
                if action == "VIEWPORT_DOWN":
                    self.scroll_down()
                if action == "SCROLL_UP":
                    self.scroll_up(4)
                if action == "SCROLL_DOWN":
                    self.scroll_down(4)
                   
                    