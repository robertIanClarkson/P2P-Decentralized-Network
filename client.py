#!/usr/bin/env python3
import socket
import pickle
from downloader import Downloader
from torrent import *

# Robert's Client from TCP Project
class Client(object):
    def __init__(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = None
        self.port = None
        self.name = None
        self.clientid = 0
        self.menu = None

        self.torrent = Torrent("age.torrent")

    def get_client_id(self):
        return self.clientid

    # connect to the server
    def connect(self, host="127.0.0.1", port=13000):
        self.clientSocket.connect((host, port))  # connect is done here
        print("(C) Successfully connected to server at {host}/{port}".format(host=host, port=port))

        self.run()

    # send data from client to CH
    def send(self, data):
        serialized_data = pickle.dumps(data)
        self.clientSocket.send(serialized_data)

    # receive data from CH
    def receive(self, MAX_BUFFER_SIZE=8192):
        try:
            data_from_client = self.clientSocket.recv(MAX_BUFFER_SIZE)
            data = pickle.loads(data_from_client)
            return data
        except: 
            print('FUCK')
            self.receive()

    """
    data = b""
    while True:
        packet = s.recv(4096)
        if not packet: break
        data += packet

    data_arr = pickle.loads(data)
    print (data_arr)
    s.close()
    """

    # close the client
    def close(self):
        self.clientSocket.close()

    def run(self):
        # client ID
        receiveData = self.receive()
        print(receiveData)

        # test data
        self.send("HELLO")

        # main logic

        downloader = Downloader(torrent=self.torrent)

        while downloader.message.next_missing_piece() is not -1:
            while downloader.message.next_missing_block(downloader.message.next_missing_piece()) is not -1:
                downloader.requestBlock(self, self.torrent.info_hash(), downloader.message.next_missing_piece(), downloader.message.next_missing_block(downloader.message.next_missing_piece()))

        print("Yay you got a full file!")

        # while piece_missing(bitfield):
        #     while block_missing(bitfield):
        #     get_block
        #     set_block_complete
        #     set_piece_complete
        #     print('File Complete') 

        # for x in range(self.torrent.num_pieces() - 1):
        #     for y in range(8):
        #         downloader.requestBlock(self, self.torrent.info_hash(), x, y)

        # while (downloader.interested):
        #     downloader.downloadNextPiece

        # downloader.compileAllPieces

        # print("File has been fully downloaded")