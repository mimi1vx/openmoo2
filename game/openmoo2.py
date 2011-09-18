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
    for parent in range(4):
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

    HOST	= OPTIONS['-h']
    PORT	= OPTIONS['-p']
    PLAYER_ID	= OPTIONS['-player']

    SOCKET_BUFFER_SIZE = 4096

    gui.GUI.init(MOO2_DIR)

    pygame.mouse.set_visible(False)
#    gui.Input().set_display(pygame.display.get_surface())

    gui.splash_screen.Screen.draw()
    gui.GUI.flip()

    networking.Client.connect(HOST, PORT, SOCKET_BUFFER_SIZE)
    networking.Client.login(PLAYER_ID)

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

#    CLIENT.ping()

    gui.GUI.run()

    networking.Client.disconnect()
# end func main

if __name__ == "__main__":
    main(sys.argv)
