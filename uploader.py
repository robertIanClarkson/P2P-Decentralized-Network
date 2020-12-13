import pickle
from file_manager import FileManager
from config import Config


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

    def send(self, data):
        serialized_data = pickle.dumps(data)
        self.clientsocket.send(serialized_data)

    def receive(self, max_alloc_mem=4096):
        serialized_data = self.clientsocket.recv(max_alloc_mem)
        data = pickle.loads(serialized_data)
        return data

    def run(self):
        # client ID
        self.send(self.client_id)

        # test data
        data = self.receive();
        print(data)

        # main logic

        while True:
            data = self.receive();
            if not data:
                continue
            print(data)

        # while True:
        #     data = receive
        #     piece = findPiece(data)
        #     send(piece)

        #     if uploadComplete:
        #         break

        # print "File has been fully uploaded!"