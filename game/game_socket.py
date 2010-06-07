import socket
import pickle
import time


class GameSocket():

    def __init__(self, socket):
        self.__socket = socket
        self.set_buffer_size(4096)
#        self.set_buffer_size(65536)
#        self.set_buffer_size(131072)
#        self.set_buffer_size(262144)

    def set_buffer_size(self, buffer_size):
        self.__buffer_size = buffer_size

    def get_buffer_size(self):
        return self.__buffer_size

    def setsockopt(self, level, optname, value):
        self.__socket.setsockopt(level, optname, value)

    def setblocking(self, flag):
        self.__socket.setblocking(flag)

    def settimeout(self, value):
        self.__socket.settimeout(value)

    def gettimeout(self):
        return self.__socket.gettimeout()

    def bind(self, address):
        self.__socket.bind(address)

    def listen(self, backlog):
        self.__socket.listen(backlog)

    def accept(self):
        client_socket, (client_host, client_port) = self.__socket.accept()
  	client_socket.setblocking(1)
        client_socket.settimeout(1)
        return GameSocket(client_socket), (client_host, client_port)

    def connect(self, address):
        self.__socket.connect(address)

    def close(self):
        self.__socket.close()

    def recv(self):
        data = "";
        chunks = 0;
        while 1:
            try:
                s = self.__socket.recv(self.get_buffer_size())
                l = len(s)
#                print("GameSocket::recv() ... received %i bytes chunk" % l)
#                s = self.clientSocket.recv(SOCKET_BUFFER_SIZE)
            except socket.timeout:
#                print("Game_client::recv ... self.clientSocket.recv > timeout")
                s = None
            if not s:
                break
            data += s
            chunks += 1
#        print("Received from server: " + data)
        l = len(data)
#        print("GameSocket::recv() ... %i chunks received" % chunks)
#        print("GameSocket::recv() ... %i bytes received" % l)
        if not l:
#            print("! ERROR: GameSocket::recv() ... returning None?")
            return None
        else:
            return pickle.loads(data)
#        return data
    # /recv
#        data = self.__socket.recv(self.get_buffer_size())
#        if not data:
#            return None
#        else:
#            return pickle.loads(data)

    def send(self, data):
#	data = "DATA ... "  + pickle.dumps(data)
        data = pickle.dumps(data)
#        return self.__socket.sendall(data)
        size = len(data)
        sent = 0
        print("# GameSocket::send() ... sending %i bytes" % (size))
        while sent < size:
            chunk_size = self.__socket.send(data[sent:])
            sent = sent + chunk_size
            print("# GameSocket::send() ... %i bytes chunk sent (total %i / %i)" % (chunk_size, sent, size))
#        time.sleep(1)
        time.sleep(self.gettimeout())
        
