import hashlib
from os import path
import shutil
from torrent import *


class FileManager:
    """
    The file manager class handles writes and reads from tmp, original and routing table.
    It also creates pointers to routing table, as well as read and write blocks/pieces of data.
    """
    TMP_FILE = "resources/tmp/age.tmp"
    DATA_FILE = "resources/tmp/blocks/blocks.data"

    def __init__(self, torrent, peer_id):
        """
        Class constructor
        :param torrent:
        :param peer_id:
        """
        self.torrent = torrent
        self.peer_id = peer_id
        self.path = self.TMP_FILE
        self.path_to_original_file = None
        self.file_size = self.torrent.file_length()
        self.piece_size = self.torrent.piece_size()
        self.hash_info = self.torrent.info_hash()

    def create_tmp_file(self):
        """
        Creates a temporal file to flush the pieces. (i.e ages.tmp)
        :return:
        """
        with open(self.path, "wb") as out:
            out.truncate(self.file_size)

    def set_path_to_original_file(self, path):
        """
        set path to resources/shared/
        :param path:
        :return:
        """
        self.path_to_original_file = path

    def hash(self, data):
        """

        :param data:
        :return:
        """
        sha1 = hashlib.sha1()
        sha1.update(data)
        data_hashed = sha1.hexdigest()
        return data_hashed

    def get_block(self, piece_index, offset, length, path=None):
        """
        DONE: gets a block from the file in the path given as parameter
        :param piece_index: the index of the piece
        :param offset: the begin offset of the block in that piece
        :param length: the length of the block
        :param path: Note that paths may be only the original file (i.e ages.txt) or
                     the tmp file (i.e ages.tmp)
        :return:
        """
        block = None
        # open file path
        file = open(path, "r")
        
        # find block using starting at (piece_index + offset)
        file.seek(piece_index + offset)
        
        # ending with start + (length)
        block = file.read(length)
        
        return block

    def get_piece(self, blocks):
        """
        Is this correct? list of blocks becomes a "b1" + "b2" ...
        DONE: Converts a list of blocks in a piece
        :param blocks: a list of blocks
        :return: the piece
        """
        piece = ""
        
        for block in blocks:
            piece += block
            
        return piece

    def flush_block(self, piece_index, block_index, block, path="resources/tmp/age.tmp"):
        """
        TODO: writes a block in blocks.data
              Each entry in routing table has the following format:
              <pointer><delimiter><block>
              pointer: A SHA1 hash of the hash info of the torrent file, piece index and block index
              delimiter: $$$
              block: the data of the block

        :param piece_index:
        :param block_index:
        :param block:
        :return: VOID
        """
        entry = str(self.pointer(
            hash_info=self.torrent.info_hash(), piece_index=piece_index, block_index=block_index)) + "$$$" + block + "\n"

        # write to the <path>
        file = open(path, "a")
        file.write(entry)
        file.close()

    def pointer(self, hash_info, piece_index, block_index):
        """
        Creates a pointer for a specific block
        :param hash_info:
        :param piece_index:
        :param block_index:
        :return:
        """
        data = str(piece_index) + str(block_index) + hash_info
        return data

    def flush_piece(self, piece_index, piece):
        """
        DONE: write a piece in tmp file once the piece is validated with the hash of the piece
        :param piece_index:
        :param piece:
        :return: VOID
        """

        tempFile = open(self.DATA_FILE, "a")
        tempFile.write(piece)
        tempFile.close()

    def get_pointers(self, hash_info, piece_index):
        """
        DONE: gets all the pointers representing a piece in the routing table
        :param hash_info:
        :param piece_index:
        :return: a list of pointers to the blocks in the same piece
        """
        tempFile = open(self.TMP_FILE, mode="r")
        lines = tempFile.readlines()
        pointers = []

        for i in range(8):
            pointer = self.pointer(hash_info=hash_info,
                                   piece_index=piece_index, block_index=i)

            for line in lines:
                filePointer = line.split("$$$")[0]
                if pointer in filePointer:
                    # print(pointer + str(":") + filePointer)
                    # print(str(piece_index) + ":" + str(i))
                    pointers.append(filePointer)

        # for line in lines:
        #     pointer = self.pointer(hash_info=hash_info,
        #                            piece_index=piece_index, block_index=block_index)
        #     for i in range(8):
        #         filePointer = line.split("$$$")[0]
        #         if pointer in filePointer:



        #     print(str(piece_index) + ":" + str(block_index))
        #     print(pointer + str(":") + filePointer)

        #     if pointer in filePointer:
        #         pointers.append(filePointer)

        #     block_index += 1

        tempFile.close()

        return pointers

    def extract_piece(self, piece_index):
        """
        DONE: extract a piece from the routing table once all the blocks from that piece are completed
        :param piece_index:
        :return: the piece
        """
        piece = ""
        piecePointers = self.get_pointers(hash_info=self.torrent.info_hash(), piece_index=piece_index)
        tmpFile = open(self.TMP_FILE, mode="r")
        pointerLines = tmpFile.readlines()
        
        for pointer in piecePointers:
            for line in pointerLines:
                if pointer in line:
                    #we got a hit on a block we need
                    piece = piece + str(line.split('$$$')[1])[:-1]

        return piece

    def piece_offset(self, piece_index):
        """
        :param piece_index:
        :return:
        """
        return piece_index * self.piece_size

    def block_offset(self, block_index, block_length):
        """
        :param block_index:
        :param block_length:
        :return:
        """
        return block_index * block_length

    def block_index(self, begin):
        return begin/self.torrent.block_size()

    def piece_validated(self, piece, piece_index):
        hashed_torrent_piece = self.torrent.piece(piece_index)
        hashed_piece = self.hash(piece)
        return hashed_torrent_piece == hashed_piece

    def move_tmp_to_shared(self):
        """
        Moves the tmp file once all the pieces from that file are downloaded to the shared folder
        :return:
        """
        file_shared_path = "resources/shared/" + self.torrent.file_name()
        if not path.exists(file_shared_path):
            shutil.move(self.path, file_shared_path)

    def path_exist(self, path_to_file):
        return path.exists(path_to_file)