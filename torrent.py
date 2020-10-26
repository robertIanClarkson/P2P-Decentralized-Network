import torrent_parser as tp
from config import Config

import hashlib

class Torrent:

    def __init__(self, torrent_path):
        self.torrent_path = torrent_path
        self.torrent_data = tp.parse_torrent_file(torrent_path)
        self.config = Config()


    def _hash_torrent_info(self, torrent_info):
        """
        Hash the torrent info from the meta-info in the torrent file.
        :param torrent_info:
        :return: the
        """
        sha1 = hashlib.sha1()
        sha1.update(torrent_info)
        return sha1.hexdigest()

    def info_hash(self):
        """
        Creates the torrent info hash (SHA1) from the info section in the torrent file
        :return:
        """

        torrent_info = self.torrent_data['info']
        hash_info = self._hash_torrent_info(str(torrent_info).encode())
        return hash_info  # returns the info hash

    def announce(self):
        return self.torrent_data['announce']

    def announce_list(self):
        return self.torrent_data['announce_list']

    def creation_date(self):
        return self.torrent_data['creation date']

    def comment(self):
        return self.torrent_data['comment']

    def created_by(self):
        return self.torrent_data['created by']

    def encoding(self):
        if self.torrent_data['encoding']:
            return self.torrent_data['encoding']
        return "encoding info not found"

    def private(self):
        # not implemented in this version
        # all the torrents in this program are public at the moment
        return 0

    def file_name(self):
        return self.torrent_data['info']['name']

    def file_length(self):
        return self.torrent_data['info']['length']

    def num_pieces(self):
        return len(self.torrent_data['info']['pieces'])

    def pieces(self):
        return self.torrent_data['info']['pieces']

    def piece(self, index):
        return self.pieces()[index]

    def piece_length(self):
        return self.torrent_data['info']['piece length']

    def validate_hash_info(self, info_hash):
        return self.info_hash() == info_hash

    def path_to_temp(self):
        torrent_path = self.torrent_path
        file = torrent_path.split('/')
        file_name = file[-1].split('.')[0]
        tmp_path = self.config.get_value("resources", "tmp-files")
        return tmp_path + file_name + ".tmp"

    def path_to_tmp_blocks(self):
        return self.config.get_value("resources", "tmp-blocks")

    def piece_size(self):
        return int(self.config.get_value("sizes", "piece-size"))

    def block_size(self):
        return int(self.config.get_value("sizes", "block-size"))