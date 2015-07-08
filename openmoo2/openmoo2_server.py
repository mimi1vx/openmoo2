import sys

import cli
import networking
import game
import rules

from openmoo2 import find_moo2_dir

def show_usage(name, message):
    print
    print(message)
    print("Usage:")
    print("	%s -g <savegame> [-h listen host] [-p listen port]" % name)
    print
# end func show_usage

def main(argv):
    """
        MAIN
    """

    default_options = {
        '-p':	9999,
        '-h':	"localhost",
        '-g':   "SAVE1.GAM"
    }

    (OPTIONS, PARAMS) = cli.parse_cli_args(argv, default_options)

    LISTEN_ADDR = OPTIONS['-h']
    LISTEN_PORT = OPTIONS['-p']
    GAME_FILE	= OPTIONS['-g']

    if GAME_FILE == "":
        show_usage(argv[0], "ERROR: Missing game file to load")
        sys.exit(1)

    print("* Init...")
    GAME = game.Game(rules.DEFAULT_RULES)

    moo2_dir = find_moo2_dir()
    if moo2_dir is not None:
        print("* Loading savegame from '%s/%s'" % (moo2_dir, GAME_FILE))
        GAME.load_moo2_savegame(moo2_dir + "/" + GAME_FILE)
#        GAME.show_stars()
#        GAME.show_planets()
        GAME.show_players()
#        GAME.show_colonies()
        GAME.show_ships()

        SERVER = networking.GameServer(LISTEN_ADDR, LISTEN_PORT, GAME)
        SERVER.set_name(GAME_FILE.split("/")[-1])

        print("* Run...")
        SERVER.run()

        print("* Exit...")
        sys.exit(0)
    else:
        print "Error: MOO2 Game directory not found in ../, ../../ or ../../../"
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv)
