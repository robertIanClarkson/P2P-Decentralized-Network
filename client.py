#!/usr/bin/env python3
import socket
import pickle

# Robert's Client from TCP Project
class Client(object):
    def __init__(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = None
        self.port = None
        self.name = None
        self.clientid = 0
        self.menu = None

    def get_client_id(self):
        return self.clientid

    # connect to the server
    def connect(self, host="127.0.0.1", port=13000):
        self.clientSocket.connect((host, port))  # connect is done here
        print("(C)Successfully connected to server at {host}/{port}".format(host=host, port=port))

    # send data from client to CH
    def send(self, data):
        serialized_data = pickle.dumps(data)
        self.clientSocket.send(serialized_data)\

    # receive data from CH
    def receive(self, MAX_BUFFER_SIZE=8192):
        data_from_client = self.clientSocket.recv(MAX_BUFFER_SIZE)
        data = pickle.loads(data_from_client)
        return data

    # close the client
    def close(self):
        self.clientSocket.close()

    def run(self):
        receiveData = self.receive()

        # get the file
        newFile = open(receiveData['file_name'], 'wb')
        newFile.write(receiveData['file_content'])

        # get the menu object
        receiveData = self.receive()
        self.menu = receiveData['menu']
        self.menu.set_client(self)

        # communicate
        while True:
            self.menu.show_menu()
            self.menu.process_user_data()

