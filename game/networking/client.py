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

class Client():

    def __init__(self, host, port, buffer_size):
        self.__socket = game_socket.GameSocket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.__socket.set_buffer_size(buffer_size)
        self.__socket.settimeout(1)
#        self.clientSocket = socket(AF_INET, SOCK_STREAM)
#        self.clientSocket.settimeout(SOCKET_TIMEOUT)
        self.__host = host
        self.__port = port
    # /__init__

    def connect(self):
        self.__socket.connect((self.__host, self.__port))
    # /connect

    def disconnect(self):
        self.__socket.close()
    # /disconnect

#    def recv(self):
#        return self.__socket.recv()

    def recv(self):
        return self.__socket.recv()

    def send(self, action, params = None):
        print("\n* ACTION: %s\nPARAMS: %s\n" % (action, str(params)))
        self.__socket.send({'action': action, 'params': params})
#        time.sleep(1)
    # /send

#    def send_data(self, data):
#	s = pickle.dumps(data)
#        print("* GameClient::send_data() ... %s" % s)
#        self.clientSocket.send(s)
#    # /send
    
    def __deprecated_recv(self):
        data = "";
        chunks = 0;
        while 1:
            try:
                s = self.recv()
#                s = self.clientSocket.recv(SOCKET_BUFFER_SIZE)
            except timeout:
                print("Game_client::recv ... self.clientSocket.recv > timeout")
                s = None
            if not s:
                break
            data += s
            chunks += 1
#        print("Received from server: " + data)
        print("GameClient::recv() ... Chunks received from game server: " + str(chunks))
        print("GameClient::recv() ... Bytes received from game server: " + str(len(data)))
        return data
    # /recv

    def __deprecated_recv_data(self):
        data = self.recv()
#        print("GameClient::recv_data() ... data = %s" % data[:20])
        if data[:9] == "DATA ... ":
            return pickle.loads(data[9:])
        else:
            return None
    # /recv_data

    def login(self, player_id):
#	print("GameClient::set_player_id() ... player_id = %s" % player_id)
        self.__player_id = player_id
        self.send("LOGIN", {'player_id': player_id})
    # /login

    def logout(self):
        self.send("LOGOUT")
    # /logout

    def get_server_name(self):
        self.send("GET_NAME")
        return self.recv()

    def fetch_game_data(self):
        self.send("FETCH_GAME_DATA")
        time.sleep(1)
        data = self.recv()
        if not data:
            print("! ERROR: GameClient::fetch_game_data() ... no data???")
        return data
    # /fetch_game_data

    def wait_for_next_turn(self):
#	print("GameClient::wait_for_next_turn()")
        self.send("NEXT_TURN")
        return True
    # /wait_for_next_turn

    def next_turn(self):
        if self.wait_for_next_turn():
 #   	    print("GameClient::next_turn()")
            response = self.recv()
            return response == "NEXT_TURN_ACK"
        else:
            print("...FAILED")
    	    return False
    # /next_turn

    def set_research(self, tech_id):
#	print("GameClient::set_research() ... tech_id = %i" % tech_id)
        self.send("SET_RESEARCH", {'tech_id': tech_id})
        return self.fetch_game_data()
    # /set_research

    def get_server_status(self):
        self.send("GET_SERVER_STATUS")
        return self.recv()
    # /get_server_status

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
    # /ping

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
