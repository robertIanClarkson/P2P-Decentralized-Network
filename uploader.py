import pickle
from pwp import PWP
from file_manager import FileManager
from config import Config


class Uploader:

    def __init__(self, peer_id, server, peer_uploader, address, torrent):
        self.peer_id = peer_id
        self.config = Config()
        self.torrent = torrent
        self.file_manager = FileManager(peer_id=peer_id, torrent=torrent)
        self.peer_uploader = peer_uploader
        self.server = server
        self.address = address
        self.pwp = PWP()
        self.peer_id = -1
        self.uploaded = 0  # bytes
        self.downloaded = 0  # bytes

        #### implement this ####
        self.uploader_bitfield = None
        self.downloader_bitfield = None

    def send(self, data):
        serialized_data = pickle.dumps(data)
        self.peer_uploader.send(serialized_data)

    def receive(self, max_alloc_mem=4096):
        serialized_data = self.peer_uploader.recv(max_alloc_mem)
        data = pickle.loads(serialized_data)
        return data