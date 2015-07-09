# vim: set ts=4 sw=4 et: coding=UTF-8

import sys
import pygame

import cli
import networking
import game
import rules
import dictionary
import autoplayer
import gui


class Orion(object):
    """
    Main object creating the game up to our likings
    """

    options = None

    def __init__(self, options): 
        self.options = options
        self.moo2_dir = OrionDataLoader.provide_lbx_datadir()

    def start_server(self):
        """
        Run all the operations required to initialize server
        """
    GAME = game.Game(rules.DEFAULT_RULES)
    GAME.load_moo2_savegame(self.moo2_dir + "/" + self.options['savegame'])
#   GAME.show_stars()
#   GAME.show_planets()
    GAME.show_players()
#   GAME.show_colonies()
    GAME.show_ships()

    SERVER = networking.GameServer(self.options['hostname'], self.options['port'], GAME)
    SERVER.set_name(GAME_FILE.split("/")[-1])
    SERVER.run()

    def start_client(self):
        """
        Run all operations to start the client
        """
        SOCKET_BUFFER_SIZE = 4096
        gui.GUI.init(self.moo2_dir)
        pygame.mouse.set_visible(False)
        gui.splash_screen.Screen.draw()
        gui.GUI.flip()
        networking.Client.connect(self.options['hostname'], self.options['port'], SOCKET_BUFFER_SIZE)
        networking.Client.login(self.options['user'])
        WINDOW_CAPTION  = "OpenMOO2: PLAYER_ID = %s" % PLAYER_ID
        pygame.display.set_caption(WINDOW_CAPTION)
        ICON = pygame.image.load(self.moo2_dir + "/orion2-icon.png")
        pygame.display.set_icon(ICON)
        gui.GUI.run()
        networking.Client.disconnect()

    def run(self):
        if option.server:
            self.start_server()
        else:
            self.start_client()

MOO2Start
