#!/usr/bin/env python3
import socket
import pickle
from downloader import Downloader
from torrent import *
import shutil
import os

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
        print(
            "(C) Successfully connected to server at {host}/{port}".format(host=host, port=port))

        self.run()

    # send data from client to CH
    def send(self, data):
        serialized_data = pickle.dumps(data)
        self.clientSocket.send(serialized_data)

    # receive data from CH
    def receive(self, MAX_BUFFER_SIZE=8192):
        data_from_client = self.clientSocket.recv(MAX_BUFFER_SIZE)
        data = pickle.loads(data_from_client)
        return data

    # close the client
    def close(self):
        self.clientSocket.close()

    def run(self):
        # client ID
        receiveData = self.receive()
        print(receiveData)

        # main logic

        downloader = Downloader(torrent=self.torrent)

        while downloader.message.next_missing_piece() is not -1:
            while downloader.message.next_missing_block(downloader.message.next_missing_piece()) is not -1:
                downloader.requestBlock(self, self.torrent.info_hash(), downloader.message.next_missing_piece(
                ), downloader.message.next_missing_block(downloader.message.next_missing_piece()))

        print("Yay you got a full file!")

        shutil.move('resources/tmp/blocks/blocks.data',
                    "downloaded/" + str(self.torrent.file_name()))
        
        shutil.move('resources/tmp/age.tmp', "resources/shared/" +
                    str(self.torrent.file_name()).split(".")[0] + ".tmp")

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
