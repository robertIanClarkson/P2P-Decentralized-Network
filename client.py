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

    # get new client info and server specs
    def getClientInfo(self, host, port):
        self.host = input("Enter the server IP Address: ")
        if self.host == "":
            self.host = host
        self.port = input("Enter the server port: ")
        if self.port == "":
            self.port = port
        self.name = input("Your id key (i.e your name): ")
        if self.name == "":
            self.name = "anonymous"

    # connect to the server
    def connect(self, host="127.0.0.1", port=13000):
        self.getClientInfo(host, port)
        self.clientSocket.connect((host, port))  # connect is done here
        print("\nSuccessfully connected to server at {host}/{port}".format(host=host, port=port))

        # handshake between client and server
        # client gets its client_id
        self.clientid = self.receive()['clientid']

        # send the name of the client to the server
        self.send(self.name)

        # log some info for the client
        print("Your client info is:")
        print("Client Name: {name}".format(name=self.name))
        print("Client ID: {id}".format(id=self.clientid))

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


# if __name__ == '__main__':
#     try:
#         client = Client()
#         client.connect()
#         client.run()
#     except KeyboardInterrupt as err:
#         print('\n(x) You left abruptly')
#     except Exception as err:
#         print('\n(x) Client Error --> {err}'.format(err=err))
#     finally:
#         exit()
