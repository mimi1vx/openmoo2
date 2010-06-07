import os.path
import os

import sys
import cli
import gui

import pygame
#from pygame.locals import *

#import lbx
import dictionary
import main_screen

import GameClient

import autoplayer

def show_usage(name, message):
    print
    print(message)
    print("Usage:")
    print(" %s -player <player id> [-h listen host] [-p listen port]" % name)
    print
# end func show_usage 


def find_moo2_dir():
    guess_dirs = ["moo2", "MOO2", "MoO2", "Moo2", "orion2", "ORION2", "Orion2", "mooii", "MOOII"]
    for parent in range(3):
        p = "../" * parent
        for d in guess_dirs:
            if os.path.isdir(p + d):
                return p + d

def main(argv):
    """
        MAIN
    """

    MOO2_DIR = find_moo2_dir()
    
    if not MOO2_DIR:
        print("")
        print("ERROR: no MOO2 directory found")
        print("    OpenMOO2 requires original Master of Orion 2 game data to run, see README.TXT for more information")
        print("")
        sys.exit(1)

#    print("Found MOO2 directory: %s" % MOO2_DIR)

    default_options = {
        '-p':       	9999,
        '-h':       	"localhost",
        '-player':  	0
    }

    (OPTIONS, PARAMS) = cli.parse_cli_args(argv, default_options)

    argc = len(argv)

#    if argc < 2:
#        show_usage(argv[0], "ERROR: No option(s) given")
#        sys.exit(1)

    HOST	= OPTIONS['-h']
    PORT	= OPTIONS['-p']
    PLAYER_ID	= OPTIONS['-player']

    DEBUG = 0

    SOCKET_BUFFER_SIZE = 4096

    GUI = gui.Gui(pygame, "sans")
    GUI.load_lbx_archives(MOO2_DIR)
    if not GUI.check_lbx_archives():
        print("")
        print("ERROR: some LBX files didn't match the expected MD5 checsum")
        print("")
        print("    The OpenMOO2 supports only original LBX files from MOO2 version 1.31")

    CLIENT = GameClient.GameClient(HOST, PORT, SOCKET_BUFFER_SIZE)
    CLIENT.connect()
    CLIENT.login(PLAYER_ID)

    server_status = CLIENT.get_server_status()
    print("# server_status = %s" % str(server_status))

    # automation for development
#    scenario = autoplayer.AutoPlayer(CLIENT)
#    scenario.play()

#    sys.exit(0)

#    WINDOW_WIDTH    = 640
#    WINDOW_HEIGHT   = 480
#    WINDOW_FLAGS	= 0
#    WINDOW_DEPTH	= 24
    WINDOW_CAPTION  = "OpenMOO2: PLAYER_ID = %s" % PLAYER_ID

    pygame.display.set_caption(WINDOW_CAPTION)

    DISPLAY = pygame.display.get_surface()

    ICON = pygame.image.load(MOO2_DIR + "/orion2-icon.png")
    pygame.display.set_icon(ICON)

    GUI.load_raw_palettes()
    GUI.init_palettes()

    PALETTES = GUI.get_palettes()
    FONTS = GUI.get_fonts()

    #    print "tested palette after loading: " + str(PALETTES['FONTS_02'])
    #    print

    IMAGES = GUI.get_images()

    GUI.load_splashscreen()
    GUI.draw_splashscreen(DISPLAY)
    pygame.display.flip()

    CLIENT.ping()

    GUI.load_graphic()

    #	COLONY VIEW

    GAME = {
        'GUI':			GUI,
        'DISPLAY':		DISPLAY,
        'PALETTES':		PALETTES,
        'IMAGES':		IMAGES,
        'FONTS':		FONTS,
        'DICTIONARY':           dictionary.get_dictionary(),
        'TURN':                 0,
        'close_game_menu':	False,
        'client':           	CLIENT
    }
    
    main_screen.run(GAME)
    GAME['client'].disconnect()
# end func main

if __name__ == "__main__":
    main(sys.argv)
