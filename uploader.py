import pickle
from file_manager import FileManager
from config import Config
from torrent import *


class Uploader:

    # whoops :)
    # def __init__(self, peer_id, server, peer_uploader, address, torrent):
        # self.peer_id = peer_id
        # self.config = Config()
        # self.torrent = torrent
        # self.file_manager = FileManager(peer_id=peer_id, torrent=torrent)
        # self.peer_uploader = peer_uploader
        # self.server = server
        # self.address = address
        # self.peer_id = -1
        # self.uploaded = 0  # bytes
        # self.downloaded = 0  # bytes

        # #### implement this ####
        # self.uploader_bitfield = None
        # self.downloader_bitfield = None

    def __init__(self, server_instance, clientsocket, addr):
        self.server_ip = addr[0]
        self.client_id = addr[1]  # important
        self.server = server_instance  # needed to use & alter <clients, names, rooms>
        self.clientsocket = clientsocket  # needed for sending and receiving

        self.torrent = Torrent("age.torrent")
        self.file_manager = FileManager(peer_id=0, torrent=self.torrent)

    def send(self, data):
        serialized_data = pickle.dumps(data)
        self.clientsocket.send(serialized_data)

    def receive(self, max_alloc_mem=4096):
        serialized_data = self.clientsocket.recv(max_alloc_mem)

        if not serialized_data:
            return " "
        data = pickle.loads(serialized_data)
        return data

    def run(self):
        # client ID
        self.send(self.client_id)

        # main logic

        while True:
            data = self.receive();

            if data == " " or not data:
                break

            print(data)
            offset = (data['piece_index'] * 16416) + data['block_index'] * 2048
            if data['piece_index'] != 0:
                offset -= 1

            block = self.file_manager.get_block(data['piece_index'], offset, 2048, "age.txt")
            response = {"piece_index": data['piece_index'], "block_index": data['block_index'], "info_hash": data['info_hash'], "block": block};
            self.send(response)