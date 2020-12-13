import threading
from file_manager import FileManager


class Downloader:

    def __init__(self, peer_downloader=None, peer_id=None, torrent=None, pwp=None, interested=None, keep_alive=None):
        self.peer_downloader = peer_downloader
        self.peer_id = peer_id
        self.torrent = torrent
        self.uploader_id = -1  # not know until the downloader runs.
        self.info_hash = self.torrent.info_hash()
        self.alive = keep_alive
        self.interested = interested
        self.file_manager = FileManager(self.torrent, self.peer_id)
        self.bitfield_lock = threading.Lock()
        self.file_lock = threading.Lock()

    def requestBlock(self, client, info_hash, piece_index, block_index):
        # request block
        message = {
            'info_hash': info_hash,
            'piece_index': piece_index,
            'block_index': block_index
        }
        client.send(message)
        block = client.receive()
        self.file_manager.flush_block(piece_index, block_index, block) 