import socket
import threading
import time
import hashlib
import pickle
import game_socket

class GameServer(object):

    def __init__(self, host, port, game):
        self.set_name("unnamed")
        self.set_host(host)
        self.set_port(port)
        self.set_socket_buffer_size(4096)
        self.__game = game
        self.__players_status = {}
        self.__threads = {}
        self.__threads_next_turn = {}
        
        for player_id in range(self.max_players()):
            self.__players_status[player_id] = 0
            
    def set_name(self, name):
        self.__name = name
        
    def get_name(self):
        return self.__name
            
    def spawn_server_socket(self):
        new_server_socket = game_socket.GameSocket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        new_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        new_server_socket.settimeout(1)
        new_server_socket.bind((self.__host, self.__port))
        new_server_socket.listen(2)
        return new_server_socket

    def log_info(self, message):
        print("# INFO: %s" % message)

    def log_debug(self, message):
        print("> DEBUG: %s" % message)

    def log_error(self, message):
        print("! ERROR: %s" % message)
            
    def __set_status(self, status):
        if status not in ["init", "turn", "recount", "shutdown"]:
            self.log_error("Server::set_status() ... bad status: %s" % status)
        else:
            self.__status = status
#	self.log_info("Server::__set_status() ... status set to \"%s\"" % status)
    
    def __get_status(self):
        return self.__status
            
    def set_turn(self):
        self.__set_status("turn")

    def set_recount(self):
        self.__set_status("recount")

    def set_shutdown(self):
        self.__set_status("shutdown")

    def check_turn(self):
        return self.__get_status() == "turn"

    def check_recount(self):
        return self.__get_status() == "recount"

    def check_shutdown(self):
        return self.__get_status() == "shutdown"

    def set_host(self, host):
        self.__host = host

    def get_host(self):
        return self.__host

    def set_port(self, port):
        self.__port = port

    def get_port(self):
        return self.__port

    def max_players(self):
        return 8;

    def set_socket_buffer_size(self, size):
        self.__socket_buffer_size = size

    def get_socket_buffer_size(self):
        return self.__socket_buffer_size

    def get_data_for_player(self, player_id):
        return self.__game.get_data_for_player(player_id)

    def send_data_to_game_client(self, client_socket, thread_id, data):
        s = pickle.dumps(data)
#	self.log_info("Server::send_data_to_game_client() ... %i bytes for thread %s" % (len(s), thread_id))
        client_socket.send(data)

    def set_next_turn(self, thread_id, player_id):
        self.__threads_next_turn[thread_id] = player_id

    def clean_next_turn(self, thread_id):
        self.set_next_turn(thread_id, -1)

    def wait_for_next_turn(self):
        pass
        
    def chech_next_turn(self):
        # chech_next_turn_multiplayer seems to work fine
        # but for now every game is supposed to be a single player
        return self.chech_next_turn_singleplayer()

    def chech_next_turn_singleplayer(self):
        # in single player human is always player_id 0
        for thread_id, player_id in self.__threads_next_turn.items():
            if player_id  == 0:
                return True
        return False

    def chech_next_turn_multiplayer(self):
        pl_st = {}
        # all the clients must confirm next turn
        for thread_id, player_id in self.__threads_next_turn.items():
            if player_id < 0:
                return False
            else:
                pl_st[player_id] = True
        self.log_info("Server::chech_next_turn() ... pl_st = %s" % str(pl_st))
        # all players must confirm next turn
        return len(pl_st) == self.__game.count_players()

    def run_client_handler(self, client_socket, thread_id):
        """
    
        """
        self.log_info("thread_id: %s\n    STARTED\n" % (thread_id))
        PLAYER_ID = -1
        socket_down = {}
        while not self.check_shutdown():
#    	    data = client_socket.recv(self.get_socket_buffer_size())
    	    data = client_socket.recv()
    	    if not data:

                # an ugly detection if the remote connection disappeared
                # explain: there is a 1s timeout, so counter should not exceed even a low number within 1 second...
                ts = int(time.time())
                if socket_down.has_key(ts):
                    socket_down[ts] += 1
                else:
                    socket_down = {ts: 1}

                if socket_down[ts] > 10:
                    self.log_info("!!! Server::run_client_handler() ... socket_down[%i] = %i" % (ts, socket_down[ts]))
                    self.log_info("!!! remote socket is down, closing local socket in thread %s" % thread_id)
                    break
                    
    	    else:
        	self.log_info("data received from client # %s, PLAYER_ID = %i" % (thread_id, PLAYER_ID))

#        	if data[:8] == "shutdown":
#		    # unsecure, just to allow clean shutdown via telnet for development
#            	    self.log_info("received shutdown!")
#		    self.set_shutdown()
#		else:

#		    data = pickle.loads(data)
                ACTION = data['action']
                PARAMS = data['params']
                    
                self.log_info("thread_id: %s\n    PLAYER_ID: %i\n    ACTION: %s\n    PARAMS: %s\n" % (thread_id, PLAYER_ID, ACTION, str(PARAMS)))

                if ACTION == "LOGIN":
                    # SECURE ME!!!
                    PLAYER_ID = PARAMS['player_id']
                    self.log_info("thread \"%s\" ... PLAYER_ID set to %i" % (thread_id, PLAYER_ID ))

                elif ACTION == "LOGOUT":
                    break

                elif ACTION == "PING":
                    self.send_data_to_game_client(client_socket,  thread_id, "PONG")

                elif ACTION == "GET_NAME":
                    self.send_data_to_game_client(client_socket,  thread_id, self.get_name())

                elif ACTION == "GET_SERVER_STATUS":
                    self.send_data_to_game_client(client_socket, thread_id, self.__get_status())

                elif ACTION == "NEXT_TURN":
                    self.log_info("received NEXT_TURN from thread %s ... player_id = %i" % (thread_id, PLAYER_ID))
                    self.set_next_turn(thread_id, PLAYER_ID)
                    self.send_data_to_game_client(client_socket,  thread_id, "NEXT_TURN_ACK")

                elif PLAYER_ID < 0:
                    self.log_error("anonymous player sending actions!!!")

                elif ACTION == "FETCH_GAME_DATA":
                    self.send_data_to_game_client(client_socket, thread_id, self.get_data_for_player(PLAYER_ID))

                elif ACTION == "SET_RESEARCH":
                    research_item = PARAMS['tech_id']
                    if not self.__game.update_research(PLAYER_ID, research_item):
                        self.log_error("Game::set_research() failed ... PLAYER_ID = %i, research_item = %i" % (PLAYER_ID, research_item))

                elif ACTION == "SET_BUILD_QUEUE":
                    if not self.__game.set_colony_build_queue(PLAYER_ID, PARAMS['colony_id'], PARAMS['build_queue']):
                        self.log_error("Game::set_colony_build_queue() failed ... PLAYER_ID = %i, colony_id = %i" % (PLAYER_ID, PARAMS['colony_id']))



                else:
                    self.log_error("unknow action received from client: '%s'" % data)

        self.log_info("thread_id: %s\n    PLAYER_ID: %i\n    CLOSING SOCKET\n" % (thread_id, PLAYER_ID))
        client_socket.close()
        self.clean_next_turn(thread_id)

    def compose_thread_id(self, client_host, client_port):
        now = str(time.time())
        s = "%s:%i@%s" % (client_host, client_port, now)
        return "%s:%s:%i" % (hashlib.md5(s).hexdigest(), client_host, client_port)

    def spawn_thread(self, client_socket, client_host, client_port):
        thread_id = self.compose_thread_id(client_host, client_port)

        th = threading.Thread(target = self.run_client_handler, args=(client_socket, thread_id))
#	thread_ident = str(th.get_ident())
    	self.log_info("Server::spawn_thread() ... new thread spawned: %s" % thread_id)
        self.__threads_next_turn[thread_id] = -1
        self.__threads[thread_id] = th
        self.__threads[thread_id].setDaemon(True)
        self.__threads[thread_id].start()
        return thread_id

    def clean_thread(self, thread_id):
        self.log_info("* Server::clean_thread() ... cleaning thread # %s" % thread_id)
        self.__threads.pop(thread_id)
        self.__threads_next_turn.pop(thread_id)

    def show_next_turns(self):
        for thread_id, player_id in self.__threads_next_turn.items():
            print("? next_turn: %s ... %i" % (thread_id, player_id))

    def debug_threads(self):
        if self.__threads:
            print("# Threads:")
            for thread_id in self.__threads:
                is_alive = self.__threads[thread_id].is_alive()
                self.log_debug("#    id = %s, is_alive = %i" % (thread_id, is_alive))

    def run(self):

        print("")
        print("PORT = %s" % self.__port)
        print("SOCKET_READ_BUFFER_SIZE = " + str(self.get_socket_buffer_size()))
        print "Awaiting connections..."
        print("")

        server_socket = self.spawn_server_socket()

        self.set_turn()

        while not self.check_shutdown():
            try:
                client_socket, (client_host, client_port) = server_socket.accept()
                thread_id = self.spawn_thread(client_socket, client_host, client_port)

            except socket.timeout:
                pass

#	    self.debug_threads()
#	    self.show_next_turns()

            if self.__threads:
                clean_threads = []
                for thread_id in self.__threads:
                    is_alive = self.__threads[thread_id].is_alive()
                    if not is_alive:
                        self.log_info("Server::run() ... thread %s is not alive, wil be cleaned" % thread_id)
                        clean_threads.append(thread_id)

                # clean old threads
                for thread_id in clean_threads:
                    self.clean_thread(thread_id)

                if self.chech_next_turn():
                    self.log_info("got True from Server::chech_next_turn() >>> DOING NEXT TURN!")
                    self.__game.next_turn()
                    # clean next turn flags for all threads
                    for thread_id in self.__threads:
                        self.clean_next_turn(thread_id)
#		else:
#		    self.log_info("# next turn not ready...")

        self.log_info("Closing serverSocket")
        server_socket.close()
