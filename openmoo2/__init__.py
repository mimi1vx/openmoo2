# vim: set ts=4 sw=4 et: coding=UTF-8

import sys
import argparse

from .orion import Orion
from .orionexception import OrionException

__version__ = '0.2.1'


def process_args(argv):
    """
    Process the parsed arguments and return the result
    :param argv: passed arguments
    """

    parser = argparse.ArgumentParser(
        prog='openmoo2', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='OpenMOO2 is opensource reimplementation of MOO2')

    parser.add_argument('-p', '--port', action='store', default=9999, type=int,
                        help='port the game will comunicate on/with')
    parser.add_argument('-h', '--hostname', action='store', default='localhost',
                        help='hostname game will work on/with')
    parser.add_argument('-u', '--user', action='store', default="player",
                        help='userid we are connecting with')
    parser.add_argument('-g', '--savegame', action='store', default='SAVE1.GAM',
                        help='savegame we want to load on server')
    parser.add_argument('-s', '--server', action='store_false',
                        help='start server instead of client')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s - {!s}'.format(__version__),
                        help='show package version and exit')

    options = parser.parse_args(args=argv)

    # convert options to simple dict
    options_dict = {
        'port': options.port,
        'hostname': options.hostname,
        'user': options.user,
        'savegame': options.savegame,
        'server': options.server,
    }

    return options_dict


def main():
    """
    Main function that calls argument parsing ensures their sanity
    and then creates main game client/server object
    """

    options = process_args(sys.argv[1:])

    try:
        orion = Orion(options)
        orion.run()
    except OrionException as exception:
        sys.stderr.write('ERROR: {0}\n'.format(exception))
        return 1
