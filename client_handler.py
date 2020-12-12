# Robert's ClientHandler
import pickle
import datetime
import threading

class ClientHandler(object):

    def __init__(self, server_instance, clientsocket, addr):
        self.server_ip = addr[0]
        self.client_id = addr[1]  # important
        self.server = server_instance  # needed to use & alter <clients, names, rooms>
        self.clientsocket = clientsocket  # needed for sending and receiving

    # send method for this thread
    def send(self, data):
        serialized_data = pickle.dumps(data)
        self.clientsocket.send(serialized_data)

    # receive method for this thread
    def receive(self, max_mem_alloc=4096):
        raw_data = self.clientsocket.recv(max_mem_alloc)
        data = pickle.loads(raw_data)
        return data

    # main process
    def run(self):
        self.send(self.client_id)

        data = self.receive();
        print(data)