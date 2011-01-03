import pygame
from _game_constants import *

import screen
import networking
import gui
import dictionary

class FleetScreen(screen.Screen):

    __view_size = 20

    __list_start = 0
    __list_size  = 0

    def __init__(self):
        screen.Screen.__init__(self)
        self.__num_fleets = 0
        self.__dict = dictionary.get_dictionary()
        self.__fleet_shown = -1

    def reset_triggers_list(self):
        screen.Screen.reset_triggers_list(self)
        self.add_trigger({'action': "ESCAPE", 'rect': pygame.Rect((558, 432), (65, 25))})
        self.add_trigger({'action': "screen", "screen": "leaders", 'rect': pygame.Rect((553, 385), (70, 20))})

        self.add_trigger({'action': "SELECT_ALL", 'rect': pygame.Rect((353, 385), (70, 20))})
        self.add_trigger({'action': "RELOCATE", 'rect': pygame.Rect((445, 385), (85, 20))})
        self.add_trigger({'action': "SCRAP", 'rect': pygame.Rect((553, 385), (70, 20))})

        self.add_trigger({'action': "filter", "filter": "support", 'rect': pygame.Rect((424, 432), (60, 20))})
        self.add_trigger({'action': "filter", "filter": "combat", 'rect': pygame.Rect((485, 432), (60, 20))})

        self.add_trigger({'action': "NEXT_FLEET", 'rect': pygame.Rect((287, 250), (25, 18))})
        self.add_trigger({'action': "PREVIOUS_FLEET", 'rect': pygame.Rect((22, 250), (25, 18))})

        self.add_trigger({'action': "SCROLL_UP", 'rect': pygame.Rect((605, 61), (15, 25))})
        self.add_trigger({'action': "SCROLL_DOWN", 'rect': pygame.Rect((605, 327), (15, 25))})
        print "fleet screen triggers reset"
        

    def get_fleets(self, ships):
        """should return a list of lists of ships that are sorted by their location"""
        ships.sort(key=lambda ship: ship.get_destination())
        fleets = [[]]
        num_fleets = 0
        dest_pos = (ships[0].get_destination() , ships[0].get_x(), ships[0].get_y())
        for ship in ships:
            ship_tup = (ship.get_destination() , ship.get_x(), ship.get_y())
            if ship_tup == dest_pos:
                fleets[num_fleets].append(ship)
            else:
                fleets.append([])
                num_fleets += 1
                fleets[num_fleets].append(ship)
                dest_pos = (ship.get_destination() , ship.get_x(), ship.get_y())
        print "FS: returning %d ships in %d"%(len(ships),num_fleets)
        return fleets

    def palette_test(self,gui):
        for i in range(17):
            ship_image = gui.GUI.get_image('SHIP', 0, i+17)
            print("test disp%d x:%d y:%d"%(i,0,i))
            gui.GUI.draw_image(ship_image,(120,25*i))

    def draw(self):
        PLAYERS = networking.Client.list_players()
        ME = networking.Client.get_me()

        players_ships = networking.Client.list_ships(ME.get_id())
        print("Player %d has %d ships" % (ME.get_id(), len(players_ships)))
        for ship in players_ships:
            if ship.exists():
                print("->name :%s %d" % (ship.get_design()['name'], ship.get_owner()))

        RULES = networking.Client.rules()
        DISPLAY = gui.GUI.get_display()

        gui.GUI.draw_image_by_key('Fleet_screen.panel', (0, 0))
        
        self.palette_test(gui)

        font2 = gui.GUI.get_font('font2')
        font3 = gui.GUI.get_font('font3')

        ship_square_x = 60 #guess of the size of the ship displayed
        ship_square_y = 60

        if len(players_ships) > 0:
            fleets = self.get_fleets(players_ships);
            self.__num_fleets = len(fleets)
            player = PLAYERS[ME.get_id()]
            if self.__fleet_shown == -1:
                current_fleet = fleets[0]
                self.__fleet_shown = 0
            else:
                if self.__fleet_shown not in range(len(fleets)):
                    current_fleet = fleets[0]
                else:
                    current_fleet = fleets[self.__fleet_shown]
                    
            current_fleet.sort(key = lambda ship: ship.get_design()['size'], reverse = True)
            for i in xrange(len(current_fleet)):
                ship = current_fleet[i];
                
                #no scrolling, just 20 ships shown, 5 rows of 4 ships
                column = i % 4 # column 0..4
                row = (i - i % 4) / 4 # row 0..5

                #here we'll add a trigger for each ship shown
                image_position = (345 + column * ship_square_x, 55 + row * ship_square_y)
                self.add_trigger({'action': "ship_info", 'ship': ship, 'rect': pygame.Rect(image_position, (ship_square_x, ship_square_y))})

                if ship.has_no_image():
                    ship.determine_image_keys(player.get_color())
                keys = ship.get_image_keys()
                print("FS: keys %d %d"%(keys[0],keys[1]))
                ship_image = gui.GUI.get_image('SHIP', keys[0], keys[1])
                print("displaying ship %d %d dest %d x:%d y:%d"%(keys[0],keys[1],ship.get_destination(),ship.get_x(),ship.get_y()))
                gui.GUI.draw_image(ship_image, image_position)

    def display_ship_info(self,ship):
        """Displays ship information text on fleet screen """

        self.draw() ##redraws the screen, to erase previous text


        dict = self.__dict
        DISPLAY = gui.GUI.get_display()
        design = ship.get_design()
        weapons = design['weapons']

        font3 = gui.GUI.get_font('font3')
        font4 = gui.GUI.get_font('font4')
        font5 = gui.GUI.get_font('font4')
        palette = [0x0, 0x181818, 0x047800]

        xpos = 15
        ypos = 285

        font5.write_text(DISPLAY, xpos, ypos, design['name'], palette, 1)
        txt= "%s (%d)"%(dict['SHIP_EXP_LEVEL'][ship.get_crew_quality()],ship.get_crew_experience())
        font4.write_text(DISPLAY, xpos, ypos +15, txt, palette, 1)
        txt = dict['SHIELDS'][design['shield']]
        font4.write_text(DISPLAY, xpos, ypos +30, txt, palette, 1)
        txt = "Beam OCV:"
        font4.write_text(DISPLAY, xpos, ypos +50, txt, palette, 1)

        xpos=170 #second column
        txt = "Beam DCV:" 
        font4.write_text(DISPLAY, xpos, ypos +50, txt, palette, 1)

        
    def scroll_up(self, step=1):
        return

    def scroll_down(self, step=1):
        return

    def view_another_fleet(self, change):
        self.__fleet_shown += change
        if self.__fleet_shown >= self.__num_fleets:
            self.__fleet_shown = 0
        elif self.__fleet_shown < 0:
            self.__fleet_shown = self.__num_fleets - 1
        print "showing fleet#%d"%self.__fleet_shown
        self.reset_triggers_list()
        self.draw()

    def process_trigger(self, trigger):

        if trigger['action'] == "SCROLL_UP":
            self.scroll_up()

        if trigger['action'] == "SCROLL_DOWN":
            self.scroll_down()
        if trigger['action'] == "NEXT_FLEET":
            self.view_another_fleet(1)
        if trigger['action'] == "PREVIOUS_FLEET":
            self.view_another_fleet(-1)
        if trigger['action'] == "ship_info":
            self.display_ship_info(trigger['ship'])

Screen = FleetScreen()
