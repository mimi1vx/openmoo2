import socket
import pickle
#from socket import *
import game_socket

import time

#SOCKET_BUFFER_SIZE = 4096
#SOCKET_BUFFER_SIZE = 1024 * 64
#SOCKET_TIMEOUT = 1

__author__="peterman"
__date__ ="$Jan 1, 2010 2:42:50 PM$"

class GameClient(object):

    def __init__(self):
        self.__socket = game_socket.GameSocket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.__socket.settimeout(1)
#        self.clientSocket = socket(AF_INET, SOCK_STREAM)
#        self.clientSocket.settimeout(SOCKET_TIMEOUT)

    def connect(self, host, port, buffer_size = 4096):
        self.__socket.set_buffer_size(buffer_size)
        self.__host = host
        self.__port = port
        self.__socket.connect((host, port))

    def disconnect(self):
        self.__socket.close()

    def recv(self):
        return self.__socket.recv()

    def send(self, action, params = None):
        print("\n* ACTION: %s\nPARAMS: %s\n" % (action, str(params)))
        self.__socket.send({'action': action, 'params': params})
    # /send

    def login(self, player_id):
#	print("GameClient::set_player_id() ... player_id = %s" % player_id)
        self.__player_id = player_id
        self.send("LOGIN", {'player_id': player_id})

    def logout(self):
        self.send("LOGOUT")

    def get_server_name(self):
        self.send("GET_NAME")
        return self.recv()

    def fetch_game_data(self):
        time.sleep(1)
        self.send("FETCH_GAME_DATA")
        self.__game_data = self.recv()
        if not self.__game_data:
            print("! ERROR: GameClient::fetch_game_data() ... no data???")
            return False
        return True

    def game_data(self):
        return self.__game_data

    def rules(self):
        return self.__game_data['rules']

    def get_galaxy(self):
        return self.__game_data['galaxy']

    def get_stardate(self):
        return self.__game_data['galaxy']['stardate']

    def list_stars(self):
        return self.__game_data['stars']

    def get_star(self, star_id):
        return self.__game_data['stars'][star_id]

    def list_stars_by_coords(self):
        return self.__game_data['stars_by_coords']

    def list_planets(self):
        return self.__game_data['planets']

    def get_planet(self, planet_id):
        return self.__game_data['planets'][planet_id]

    def list_colonies(self):
        return self.__game_data['colonies']

    def get_colony(self, colony_id):
        return self.__game_data['colonies'][colony_id]

    def list_ship_ids(self):
        """returns all ships as a list of ship_id's (old method)"""
        return self.__game_data['ships']

    def list_ships(self,player_id=-1):
        """returns ships of one player as a list of starship objects
        """
        ships=[]
        for ship_id in self.__game_data['ships']:
            ship = self.__game_data['ships'][ship_id]
            player = self.__game_data['players'][ship.get_owner()]
            if ship.has_no_image() and hasattr(player, '__color'):
                col = player.get_color()
                ship.determine_image_keys(col)
            if ship.get_owner() == player_id and ship.exists():
                ships.append(ship)
        return ships

    def list_prototypes(self):
        return self.__game_data['prototypes']

    def list_officers(self):
        return self.__game_data['officers']

    def list_colony_leaders(self):
        return self.__game_data['colony_leaders']

    def list_players(self):
        return self.__game_data['players']

    def get_player(self, player_id):
        return self.__game_data['players'][player_id]

    def get_me(self):
        return self.__game_data['me']

    def wait_for_next_turn(self):
#	print("GameClient::wait_for_next_turn()")
        self.send("NEXT_TURN")
        return True

    def next_turn(self):
        if self.wait_for_next_turn():
 #   	    print("GameClient::next_turn()")
            response = self.recv()
            return response == "NEXT_TURN_ACK"
        else:
            print("...FAILED")
    	    return False

    def set_research(self, tech_id):
#	print("GameClient::set_research() ... tech_id = %i" % tech_id)
        self.send("SET_RESEARCH", {'tech_id': tech_id})
        return self.fetch_game_data()

    def get_server_status(self):
        self.send("GET_SERVER_STATUS")
        return self.recv()

    def ping(self):
        tm1 = time.time()
        self.send("PING")
        ping_response = self.recv()
        tm2 = time.time()
        ping_time = round(tm2 - tm1, 2)
        if ping_response == "PONG":
            print("PING: %ss" % (ping_time))
        else:
            print("PING: WRONG RESPONSE '%s' returned in %ss" % (ping_response, ping_time))


    def set_colony_build_queue(self, colony_id, build_queue):
        """ Sends the new build queue for given player's colony """
        self.send("SET_BUILD_QUEUE", {'colony_id': colony_id, 'build_queue': build_queue})
        return self.fetch_game_data()
        
"""
    def get_game_data(self):
        self.send("GET_GAME")
        return self.recv()

    def list_players(self):
        self.send("LIST_PLAYERS")
        return self.recv()

    def fetch_galaxy_info(self):
        self.send("GET_GALAXY_INFO")
        return self.recv()

    def list_stars(self):
        self.send("LIST_STARS")
        return self.recv()

    def list_planets(self):
        self.send("LIST_PLANETS")
        return self.recv()

    def list_colonies(self):
        self.send("LIST_COLONIES")
        return self.recv()
"""

Client = GameClient()