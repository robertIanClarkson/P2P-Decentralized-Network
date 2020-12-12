# File: tracker.py
# Author: <your name here>
# SID: <your student id here>
# Date: <the date when this file was last updated/created/edited>
# Description: this file contains the implementation of the tracker class.

import bencodepy
import socket
import threading

import uuid # to generate an ID
import time # for timestamp

class Tracker:
    """
    This class contains methods that provide implementations to support trackerless peers
    supporting the DHT and KRPC protocols
    """

    DHT_PORT = 12001

    def __init__(self, peer, server, torrent, announce=True):
        """
        TODO: Add more work here as needed.
        :param server:
        :param torrent:
        :param announce:
        """
        self._id = int(uuid.uuid1())
        self._peer = peer
        self._server = server
        self._torrent = torrent
        self._is_announce = announce
        # self._clienthandler = server.clienthandlers[0]
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.udp_socket.bind(("", self.DHT_PORT))
        # will story a list of dictionaries representing entries in the routing table
        # dictionaries stored here are in the following form
        # {'nodeID': '<the node id is a SHA1 hash of the ip_address and port of the server node and a random uuid>',
        #  'ip_address': '<the ip address of the node>', 'port': '<the port number of the node',
        #  'info_hash': '<the info hash from the torrent file>', last_changed': 'timestamp'}
        # self._routing_table = []
        self.peers = []

    def broadcast(self, message, self_broadcast_enabled=False):
        try:
            # print(f'Broadcast: {message}')
            encoded_message = self.encode(message)
            self.udp_socket.sendto(encoded_message, ('<broadcast>', self.DHT_PORT))
            print(f'(T) Broadcasting...')
        except socket.error as error:
            print(f'(T) Error broadcasting on port ({self.DHT_PORT}) --> {err}')

    def send_udp_message(self, message, ip, port):
        try:
            print(f'(T) sent UDP message --> {ip}:{port}')
            self.printQuery(message)
            new_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            message = self.encode(message)
            new_socket.sendto(message, (ip, port))
        except Exception as err:
            print(f'(T) Error sending UDP message --> {err}')

    def broadcast_listener(self):
        try:
            print(f'(T) Listening at DHT port --> {self.DHT_PORT}')
            while True:
                raw_data, sender_ip_and_port = self.udp_socket.recvfrom(4096)
                if raw_data:
                    data = self.decode(raw_data)
                    ip_sender = sender_ip_and_port[0]
                    port_sender = sender_ip_and_port[1]
                    print(f'(T) data recieved')
                    # print(f'data recieved by sender')
                    self.process_query(data, ip_sender, port_sender)
        except Exception as err:
            print(f"(T) Error listening at port ({self.DHT_PORT}) --> {err}")

    #############################################################
    def process_query(self, data, ip, port):
        print(f"(T) {ip} | {port} | {data}")
        is_new_peer = self.addPeer(data, ip)
        if is_new_peer: # connect to its server
            print('(T) Added a new Peer')
            self._peer._connect_to_peer(data['port'], data['ip'], data['port'])
    #############################################################

    def addPeer(self, data, new_peer_ip):
        new_peer_id = data['id']
        new_peer_port = data['port']

        # check to see if we have peer
        for peer in self.peers:
            if peer['id'] == new_peer_id:
                print(f'(T) Peer already tracked --> id: {new_peer_id}')
                return False
        
        # we dont have peer
        peer = {
            'id': new_peer_id,
            'ip': new_peer_ip,
            'port': new_peer_port,
            'connected': False
        }
        self.peers.append(peer)
        return True

    def encode(self, message):
        """
        bencodes a message
        :param message: a dictionary representing the message
        :return: the bencoded message
        """
        return bencodepy.encode(message)


    def decode(self, bencoded_message):
        """
        Decodes a bencoded message
        :param bencoded_message: the bencoded message
        :return: the original message
        """
        bc = bencodepy.Bencode(encoding='utf-8')
        return bc.decode(bencoded_message)
 

    def run(self, start_with_broadcast=True):
        # start listening
        threading.Thread(target=self.broadcast_listener).start()

        # announce me
        message = {
            'id': self._id,
            'ip': self._server.host,
            'port': self._server.port
        }
        self.broadcast(message)


