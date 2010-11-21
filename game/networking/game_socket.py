import socket
import pickle
import time

class GameSocket(object):

    def __init__(self, socket):
        self.__socket = socket
        self.set_buffer_size(4096)
        self.__head_size = 64
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

    def __recv_raw(self, data_size):
        data = ""
        buffer_size = self.get_buffer_size()
        while data_size:
            try:
                chunk = self.__socket.recv(min(buffer_size, data_size))
            except socket.timeout:
                chunk = ""
            if not chunk:
                break
            data += chunk
            data_size -= len(chunk)
        return data

    def recv(self):
        head_raw = self.__recv_raw(self.__head_size).rstrip()
        # return None if header is empty
        if not head_raw:
            return None
        head = pickle.loads(head_raw)
        return pickle.loads(self.__recv_raw(head['data_size']))

    def __compose_head(self, data_size):
        return pickle.dumps({
            'data_size':    data_size
        }).ljust(self.__head_size)

    def send(self, data):
        data = pickle.dumps(data)
        head = self.__compose_head(len(data))
        data = head + data
        total_size = len(data)
        sent = 0
        while sent < total_size:
            chunk_size = self.__socket.send(data[sent:])
            sent = sent + chunk_size
