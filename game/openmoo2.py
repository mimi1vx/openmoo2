import os.path
import os

import sys
import cli

import pygame

import dictionary

import networking

import autoplayer

import gui

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

    SOCKET_BUFFER_SIZE = 4096

    GUI = gui.Gui(pygame, MOO2_DIR)

    pygame.mouse.set_visible(False)
    gui.Input().set_display(pygame.display.get_surface())

    SCREENS = {
        'FONTS':            gui.FontsScreen(GUI),
        'SPLASH':           gui.SplashScreen(GUI),
        'MAIN':             gui.MainScreen(GUI),
        'STARSYSTEM':       gui.StarsystemScreen(GUI),
        'COLONIES':         gui.ColoniesScreen(GUI),
        'PLANETS':          gui.PlanetsScreen(GUI),
        'RESEARCH':         gui.ResearchScreen(GUI),
        'LEADERS':          gui.LeadersScreen(GUI),
        'COLONY':           gui.ColonyScreen(GUI),
        'COLONY_BUILD':     gui.ColonyBuildScreen(GUI),
        'INFO':             gui.InfoScreen(GUI)
    }

    for screen_key, screen_object in SCREENS.items():
        screen_object.attach_screens(SCREENS)

    SCREENS['SPLASH'].run()

    CLIENT = networking.Client(HOST, PORT, SOCKET_BUFFER_SIZE)
    CLIENT.connect()
    CLIENT.login(PLAYER_ID)

#    server_status = CLIENT.get_server_status()
#    print("# server_status = %s" % str(server_status))

    # automation for development
#    scenario = autoplayer.AutoPlayer(CLIENT)
#    scenario.play()

#    sys.exit(0)

    WINDOW_CAPTION  = "OpenMOO2: PLAYER_ID = %s" % PLAYER_ID

    pygame.display.set_caption(WINDOW_CAPTION)
    
    ICON = pygame.image.load(MOO2_DIR + "/orion2-icon.png")
    pygame.display.set_icon(ICON)

#    PALETTES = GUI.get_palettes()

    #    print "tested palette after loading: " + str(PALETTES['FONTS_02'])
    #    print

#    CLIENT.ping()

#    GUI.load_graphic()

    #	COLONY VIEW

    GAME = {
#        'GUI':			GUI,
#        'PALETTES':		PALETTES,
#        'IMAGES':		IMAGES,
        'DICTIONARY':           dictionary.get_dictionary(),
        'TURN':                 0,
        'close_game_menu':	False,
        'client':           	CLIENT
    }

    SCREENS['MAIN'].run(GAME)

#    main_screen.run(GAME)
    GAME['client'].disconnect()
# end func main

if __name__ == "__main__":
    main(sys.argv)
