#!/usr/bin/env python3
import socket
import pickle
from downloader import Downloader
from torrent import *
import shutil
import os
from htpbs import ProgressBars, Work

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

    def work(self, progressbars, bar_index, work_value, work_name):
        """

        :param progressbars: the progressbar obkect
        :param bar_index: a integer representing the index of the bae
        :param work_value: a value for time.sleep() to simulate different progress bars rates
        :param work_name: the name of the work
        :return: VOID
        """
        progressbars.set_bar_prefix(bar_index=bar_index, prefix=work_name)
        # client ID
        receiveData = self.receive()
        print(receiveData)

        # main logic

        downloader = Downloader(torrent=self.torrent)

        i = 0
        while downloader.message.next_missing_piece() is not -1:
            while downloader.message.next_missing_block(downloader.message.next_missing_piece()) is not -1:
                downloader.requestBlock(self, self.torrent.info_hash(), downloader.message.next_missing_piece(
                ), downloader.message.next_missing_block(downloader.message.next_missing_piece()))
                progressbars.update(bar_index=bar_index, value=i * 100)
                i += work_value

        progressbars.finish()

        progressbars.clear_bar(bar_index=bar_index) 

        print("Yay you got a full file!")

        shutil.move('resources/tmp/blocks/blocks.data',
                    "downloaded/" + str(self.torrent.file_name()))

        shutil.move('resources/tmp/age.tmp', "resources/shared/" +
                    str(self.torrent.file_name()).split(".")[0] + ".tmp")

    def run(self):
        work_increments = 1/(self.torrent.num_pieces() * 8)
        progressbars = ProgressBars(num_bars=1)
        
        Work.start(self.work, (progressbars, 0, work_increments,
                          self.torrent.file_name() + ": "))
        
