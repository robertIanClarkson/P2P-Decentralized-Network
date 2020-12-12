from server import Server
import hashlib
import bencodepy
import socket
import threading
import time
import datetime
import hashlib
import uuid


class Tracker:
    def __init__(self, server, torrent):
        self.server = server
        self._torrent = torrent
        self.torrent_info_hash = self._get_torrent_info_hash()
        self.UDP_broadcast_socket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM)
        self.UDP_broadcast_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.UDP_broadcast_socket.bind(("", self.DHT_PORT))
        self._clienthandler = None  # server.client_handlers[0]
        self.print_lock = threading.Lock()  # creates the print lock
        self.nodes = []
        self.peer_id = str(peerId)

        # will store a list of dictionaries representing entries in the routing table
        # dictionaries stored here are in the following form
        # {'nodeID': '<the node id is a SHA1 hash of the ip_address and port of the server node and a random uuid>',
        #  'ip_address': '<the ip address of the node>', 'port': '<the port number of the node',
        #  'info_hash': '<the info hash from the torrent file>', last_changed': 'timestamp'}
        self._routing_table = [{self._torrent.info_hash(): []}]

    def _get_torrent_info_hash(self):
        """
        DONE: creates the torrent info hash (SHA1) from the info section in the torrent file
        :return:
        """
        return self._torrent.info_hash()  # returns the info hash

    def add_peer_to_swarm(self, peer_id, peer_ip, peer_port):
        """
        TODO: when a peers connects to the network adds this peer
              to the list of peers connected
        :param peer_id:
        :param peer_ip:
        :param peer_port:
        :return:
        """
        # this is a new node, I should respond by asking for get_peers()
        responseWithNodes = {"t": "aa",
                             "y": "r",
                             "r": {
                                 "id": query['a']['id'],
                                 "token": "aoeusnth", "values": self._routing_table[0][self._torrent.info_hash()]}}

        self.send_response(responseWithNodes, source_ip)

    def remove_peer_from_swarm(self, peer_id):
        """
        TODO: removes a peer from the swarm when it disconnects from the network
              Note: this method needs to handle exceptions when the peer disconnected abruptly without
              notifying the network (i.e internet connection dropped...)
        :param peer_id:
        :return:
        """
        normalPingResponse = {"t": "aa",
                              "y": "r", "r": {"id": self.peer_id}}

        # self.printThis("Response = {}".format(normalPingResponse))
        self.send_response(normalPingResponse, source_ip)

    def send_response(self, message, destination_ip):
        """
        send a response to a specific node
        :return:
        """
        try:
            self.UDP_broadcast_socket.sendto(self.encode(
                message), (destination_ip, self.DHT_PORT))

        except Exception as e:
            print("exception sending response ", e)

    def findAndCreate(self, hash_info, ip, port):
        """
        This function should take th IP and port and check
        if the node has been discovered or not.
        :return: true if node exists
        else false
        """
        nodesList = None
        index = 0

        for node in self._routing_table:
            if(hash_info in node.keys()):
                nodesList = node[hash_info]
                break
            index += 1

        port = int(port)
        for node in nodesList:
            if node['ip'] == ip and node['port'] == port:
                return True

        nodesList.append({
            'nodeId': self._hash({'ip': ip, 'port': port, 'uuid': uuid.uuid4()}),
            'ip': ip,
            "port": port,
            'last_changed': str(datetime.datetime.now())})
        self._routing_table[0][hash_info] = nodesList

        return False

    def broadcast(self, message, self_broadcast_enabled=False):
        self.printThis("Query = {}".format(message))
        encoded_message = self.encode(message)
        self.printThis("Query bencoded = {}".format(encoded_message))
        self.UDP_broadcast_socket.sendto(
            encoded_message, ("<broadcast>", self.DHT_PORT))

    def set_total_uploaded(self, peer_id):
        """
        TODO: sets the total data uploaded so far by the peer passed as a parameter
        :param peer_id:
        :return: VOID
        """
        pass  # your code here

    def total_downloaded(self, peer_id):
        """
        TODO: sets the total data downloaded so far by the peer passed as a parameter
        :param peer_id:
        :return: VOID
        """
        pass  # your code here

    def validate_torrent_info_hash(self, peer_torrent_info_hash):
        """
        DONE: compare the info_hash generated by this peer with another info_hash sent by another peer
              this is done to make sure that both peers agree to share the same file.
        :param peer_torrent_info_hash: the info_hash from the info section of the torrent sent by other peer
        :return: True if the info_hashes are equal. Otherwise, returns false.
        """
        return peer_torrent_info_hash == self._get_torrent_info_hash()

    def encode(self, message):
        """
        "        bencodes a message"
        "        : param message: a dictionary representing the message"
        "        : return: the bencoded message"
        """
        return bencodepy.encode(message)


def decode(self, bencoded_message):
    """
"        Decodes a bencoded message"
"        : param bencoded_message: the bencoded message"
"        : return: the original message"
"""
    bc = bencodepy.Bencode(encoding='utf-8')

    return bc.decode(bencoded_message)

    def broadcast_listener(self):
        """
        ": return:"
        """
        print("Tracker is listening at port {}".format(self.DHT_PORT))
        try:
            while True:
                raw_data, sender_ip_port = self.UDP_broadcast_socket.recvfrom(
                    4096)
                self.printThis("Response bencoded = {}".format(raw_data))
                data = self.decode(raw_data)
                self.printThis("Response = {}".format(data))
                self.process_query(data, sender_ip_port[0], sender_ip_port[1])

        except Exception as e:
            print("exception broadcasting ", e)

    def printThis(self, message):
        self.print_lock.acquire()
        print(message)
        self.print_lock.release()

    # def ping(self, t, y, a: dict = None, r=None):
    #     if not a:
    #         a = {'id': self._torrent.info_hash()}
    #     return {"t": t, "y": t, "q": "ping", "a": a}

    def ping(self, t, y, a: dict = None, r=None):
        """
    "        implement the ping method"
    "        : param t:"
    "        : param y:"
    "        : param a:"
    "        : return:"
    """

        if not a:
            a = {'id': self._torrent.info_hash()}

        return {"t": t, "y": t, "q": "ping", "a": a}

    def find_node(self, t, y, a=None, r=None):
        """
        "implement the find_node method"
        ": return:"
        """
        return {"t": t,
                "y": y,
                "q": "find_node",
                "a": {
                    "id":  self._routing_table[0][self._torrent.info_hash()][0]['nodeId'],
                    # JUST USED FOR TESTING!!
                    "target": self._routing_table[0][self._torrent.info_hash()][0]['nodeId']
                }
                }

    def get_peers(self, t, y, a: dict = None, r=None):
        """
        "implement the get_peers method"
        ": return:"
        """
        if not a:
            a = {
                "id": self.peer_id,
                "info_hash": self._torrent.info_hash()
            }
        query = {"t": t,
                 "y": y,
                 "q": "get_peers",
                 "a": a
                 }

        return query

    def announce_peers(self, t, y, a=None, r=None):
        """
        "implement the announce_peers method"
        ": return:"
        """
        return {"t": "aa", "y": "q", "q": "announce_peer", "a": {"id": "abcdefghij0123456789", "implied_port": 1, "info_hash": "mnopqrstuvwxyz123456", "port": 6881, "token": "aoeusnth"}}

    def get_node_info(self, nodeId):
        for row in self._routing_table:
            for nodes in row.values():
                for node in nodes:
                    if(nodeId in node['nodeId']):
                        return node

    def process_query(self, query, source_ip, source_port):
        """
        "process an incoming query from a node"
        ": return: the response"
        """

        if 'q' in query.keys():
            if query['q'] == "ping":
                # print("validating hash..: ",
                #       self._torrent.validate_hash_info(query['a']['id']))
                nodeExists = self.findAndCreate(
                    self._torrent.info_hash(), source_ip, source_port)
                if not nodeExists:
                    # this is a new node, I should respond by asking for get_peers()
                    responseWithNodes = {"t": "aa",
                                         "y": "r",
                                         "r": {
                                             "id": query['a']['id'],
                                             "token": "aoeusnth", "values": self._routing_table[0][self._torrent.info_hash()]}}

                    self.send_response(responseWithNodes, source_ip)
                else:
                    normalPingResponse = {"t": "aa",
                                          "y": "r", "r": {"id": self.peer_id}}

                    # self.printThis("Response = {}".format(normalPingResponse))
                    self.send_response(normalPingResponse, source_ip)

            elif query['q'] == "find_node":
                nodeFound = self.get_node_info(query['a']['target'])
                response = {
                    "t": "aa",
                    "y": "r",
                    "r": {
                        "id": source_ip,
                        "nodes": nodeFound
                    }
                }
                # self.printThis("Response = {}".format(response))
                self.send_response(response, source_ip)
            elif query['q'] == "get_peers":
                self.send_response({"t": "aa", "y": "r", "r": {
                                   "id": self.peer_id, "token": "aoeusnth", "values": ["axje.u", "idhtnm"]}}, source_ip)
            elif query['q'] == "announce_peers":
                self.send_response({"t": "aa", "y": "r", "r": {
                                   "id": source_ip}}, source_ip)

    def send_response(self, message, destination_ip):
        """
        "send a response to a specific node"
        ": return:"
        """
        try:
            self.UDP_broadcast_socket.sendto(self.encode(
                message), (destination_ip, self.DHT_PORT))

        except Exception as e:
            print("exception sending response ", e)

    def findAndCreate(self, hash_info, ip, port):
        """
        "This function should take th IP and port and check"
        "if the node has been discovered or not."
        ": return: true if node exists"
        "else false"
        """
        nodesList = None
        index = 0

        for node in self._routing_table:
            if(hash_info in node.keys()):
                nodesList = node[hash_info]
                break
            index += 1

        port = int(port)
        for node in nodesList:
            if node['ip'] == ip and node['port'] == port:
                return True

        nodesList.append({
            'nodeId': self._hash({'ip': ip, 'port': port, 'uuid': uuid.uuid4()}),
            'ip': ip,
            "port": port,
            'last_changed': str(datetime.datetime.now())})
        self._routing_table[0][hash_info] = nodesList

        return False

    def get_node_info(self, nodeId):
        for row in self._routing_table:
            for nodes in row.values():
                for node in nodes:
                    if(nodeId in node['nodeId']):
                        return node

    def _hash(self, dictionary: dict):
        sha1 = hashlib.sha1()
        sha1.update(str(dictionary).encode('utf-8'))
        return sha1.hexdigest()

    def send_response(self, message, destination_ip):
        """
        "send a response to a specific node"
        ": return:"
        """
        try:
            self.UDP_broadcast_socket.sendto(self.encode(
                message), (destination_ip, self.DHT_PORT))

        except Exception as e:
            print("exception sending response ", e)

    def find_node(self, t, y, a=None, r=None):
        """
        "implement the find_node method"
        ": return:"
        """
        return {"t": t,
                "y": y,
                "q": "find_node",
                "a": {
                    "id":  self._routing_table[0][self._torrent.info_hash()][0]['nodeId'],
                    # JUST USED FOR TESTING!!
                    "target": self._routing_table[0][self._torrent.info_hash()][0]['nodeId']
                }
                }

    def get_peers(self, t, y, a: dict = None, r=None):
        """
        "implement the get_peers method"
        ": return:"
        """
        if not a:
            a = {
                "id": self.peer_id,
                "info_hash": self._torrent.info_hash()
            }
        query = {"t": t,
                 "y": y,
                 "q": "get_peers",
                 "a": a
                 }

        return query

    def announce_peers(self, t, y, a=None, r=None):
        """
        "implement the announce_peers method"
        ": return:"
        """
        return {"t": "aa", "y": "q", "q": "announce_peer", "a": {"id": "abcdefghij0123456789", "implied_port": 1, "info_hash": "mnopqrstuvwxyz123456", "port": 6881, "token": "aoeusnth"}}

    def run(self, start_with_broadcast=True):
        """
"This function is called from the peer.py to start this tracker"
": return: VOID"
"""
        threading.Thread(target=self.broadcast_listener).start()
        if self._is_announce == True:
            # start the process of pinging.
            pingMessage = self.ping("aa", "q", r=None)
            self.broadcast(pingMessage)
            time.sleep(1)
            self.printThis("*********************\n\n")

            findNodeMessage = self.find_node("aa", "q")
            self.broadcast(findNodeMessage)
            time.sleep(1)
            self.printThis("*********************\n\n")

            getPeerMessage = self.get_peers("aa", "q")
            self.broadcast(getPeerMessage)
            time.sleep(1)
            self.printThis("*********************\n\n")

            announcePeersMessage = self.announce_peers("aa", "q")
            self.broadcast(announcePeersMessage)
            time.sleep(1)

        else:
            print("This tracker does not support DHT")


############################################################################

# """
# # File: tracker.py
# # Author: Ramy fekry
# # SID: 917013453
# # Date: 11/10/2020
# # Description: this file contains the implementation of the tracker class.

# import bencodepy
# import socket
# import threading
# import time
# import datetime
# import hashlib
# import uuid


# class Tracker:
#     """
# "This class contains methods that provide implementations to support trackerless peers"
# "supporting the DHT and KRPC protocols"
# """
#     DHT_PORT = 12001

#     def __init__(self, server, torrent, peerId, announce=True, client=None):
#         """
# "TODO: Add more work here as needed."
# ": param server:"
# "    : param torrent:"
# "        : param announce:"
#         """
#         self._server = server
#         self._torrent = torrent
#         self._is_announce = announce
#         self.client = client
#         self.UDP_broadcast_socket = socket.socket(
#             socket.AF_INET, socket.SOCK_DGRAM)
#         self.UDP_broadcast_socket.setsockopt(
#             socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#         self.UDP_broadcast_socket.bind(("", self.DHT_PORT))
#         self._clienthandler = None  # server.client_handlers[0]
#         self.print_lock = threading.Lock()  # creates the print lock
#         self.nodes = []
#         self.peer_id = str(peerId)

#         # will store a list of dictionaries representing entries in the routing table
#         # dictionaries stored here are in the following form
#         # {'nodeID': '<the node id is a SHA1 hash of the ip_address and port of the server node and a random uuid>',
#         #  'ip_address': '<the ip address of the node>', 'port': '<the port number of the node',
#         #  'info_hash': '<the info hash from the torrent file>', last_changed': 'timestamp'}
#         self._routing_table = [{self._torrent.info_hash(): []}]

#     def printThis(self, message):
#         self.print_lock.acquire()
#         print(message)
#         self.print_lock.release()

#     def broadcast(self, message, self_broadcast_enabled=False):
#         self.printThis("Query = {}".format(message))
#         encoded_message = self.encode(message)
#         self.printThis("Query bencoded = {}".format(encoded_message))
#         self.UDP_broadcast_socket.sendto(
#             encoded_message, ("<broadcast>", self.DHT_PORT))

#     def encode(self, message):
#         """
# "        bencodes a message"
# "        : param message: a dictionary representing the message"
# "        : return: the bencoded message"
#         """
#         return bencodepy.encode(message)

#     def decode(self, bencoded_message):
#         """
# "        Decodes a bencoded message"
# "        : param bencoded_message: the bencoded message"
# "        : return: the original message"
#         """
#         bc = bencodepy.Bencode(encoding='utf-8')

#         return bc.decode(bencoded_message)

#     def ping(self, t, y, a: dict = None, r=None):
#         """
# "        implement the ping method"
# "        : param t:"
# "        : param y:"
# "        : param a:"
# "        : return:"
#         """

#         if not a:
#             a = {'id': self._torrent.info_hash()}

#         return {"t": t, "y": t, "q": "ping", "a": a}

#     def find_node(self, t, y, a=None, r=None):
#         """
#         "implement the find_node method"
#         ": return:"
#         """
#         return {"t": t,
#                 "y": y,
#                 "q": "find_node",
#                 "a": {
#                     "id":  self._routing_table[0][self._torrent.info_hash()][0]['nodeId'],
#                     # JUST USED FOR TESTING!!
#                     "target": self._routing_table[0][self._torrent.info_hash()][0]['nodeId']
#                 }
#                 }

#     def get_peers(self, t, y, a: dict = None, r=None):
#         """
#         "implement the get_peers method"
#         ": return:"
#         """
#         if not a:
#             a = {
#                 "id": self.peer_id,
#                 "info_hash": self._torrent.info_hash()
#             }
#         query = {"t": t,
#                  "y": y,
#                  "q": "get_peers",
#                  "a": a
#                  }

#         return query

#     def announce_peers(self, t, y, a=None, r=None):
#         """
#         "implement the announce_peers method"
#         ": return:"
#         """
#         return {"t": "aa", "y": "q", "q": "announce_peer", "a": {"id": "abcdefghij0123456789", "implied_port": 1, "info_hash": "mnopqrstuvwxyz123456", "port": 6881, "token": "aoeusnth"}}

#     def get_node_info(self, nodeId):
#         for row in self._routing_table:
#             for nodes in row.values():
#                 for node in nodes:
#                     if(nodeId in node['nodeId']):
#                         return node

#     def process_query(self, query, source_ip, source_port):
#         """
#         "process an incoming query from a node"
#         ": return: the response"
#         """

#         if 'q' in query.keys():
#             if query['q'] == "ping":
#                 # print("validating hash..: ",
#                 #       self._torrent.validate_hash_info(query['a']['id']))
#                 nodeExists = self.findAndCreate(
#                     self._torrent.info_hash(), source_ip, source_port)
#                 if not nodeExists:
#                     # this is a new node, I should respond by asking for get_peers()
#                     responseWithNodes = {"t": "aa",
#                                          "y": "r",
#                                          "r": {
#                                              "id": query['a']['id'],
#                                              "token": "aoeusnth", "values": self._routing_table[0][self._torrent.info_hash()]}}

#                     self.send_response(responseWithNodes, source_ip)
#                 else:
#                     normalPingResponse = {"t": "aa",
#                                           "y": "r", "r": {"id": self.peer_id}}

#                     # self.printThis("Response = {}".format(normalPingResponse))
#                     self.send_response(normalPingResponse, source_ip)

#             elif query['q'] == "find_node":
#                 nodeFound = self.get_node_info(query['a']['target'])
#                 response = {
#                     "t": "aa",
#                     "y": "r",
#                     "r": {
#                         "id": source_ip,
#                         "nodes": nodeFound
#                     }
#                 }
#                 # self.printThis("Response = {}".format(response))
#                 self.send_response(response, source_ip)
#             elif query['q'] == "get_peers":
#                 self.send_response({"t": "aa", "y": "r", "r": {
#                                    "id": self.peer_id, "token": "aoeusnth", "values": ["axje.u", "idhtnm"]}}, source_ip)
#             elif query['q'] == "announce_peers":
#                 self.send_response({"t": "aa", "y": "r", "r": {
#                                    "id": source_ip}}, source_ip)

#     def send_response(self, message, destination_ip):
#         """
#         "send a response to a specific node"
#         ": return:"
#         """
#         try:
#             self.UDP_broadcast_socket.sendto(self.encode(
#                 message), (destination_ip, self.DHT_PORT))

#         except Exception as e:
#             print("exception sending response ", e)

#     def findAndCreate(self, hash_info, ip, port):
#         """
#         "This function should take th IP and port and check"
#         "if the node has been discovered or not."
#         ": return: true if node exists"
#         "else false"
#         """
#         nodesList = None
#         index = 0

#         for node in self._routing_table:
#             if(hash_info in node.keys()):
#                 nodesList = node[hash_info]
#                 break
#             index += 1

#         port = int(port)
#         for node in nodesList:
#             if node['ip'] == ip and node['port'] == port:
#                 return True

#         nodesList.append({
#             'nodeId': self._hash({'ip': ip, 'port': port, 'uuid': uuid.uuid4()}),
#             'ip': ip,
#             "port": port,
#             'last_changed': str(datetime.datetime.now())})
#         self._routing_table[0][hash_info] = nodesList

#         return False

#     def _hash(self, dictionary: dict):
#         sha1 = hashlib.sha1()
#         sha1.update(str(dictionary).encode('utf-8'))
#         return sha1.hexdigest()

#     def broadcast_listener(self):
#         """
#         ": return:"
#         """
#         print("Tracker is listening at port {}".format(self.DHT_PORT))
#         try:
#             while True:
#                 raw_data, sender_ip_port = self.UDP_broadcast_socket.recvfrom(
#                     4096)
#                 self.printThis("Response bencoded = {}".format(raw_data))
#                 data = self.decode(raw_data)
#                 self.printThis("Response = {}".format(data))
#                 self.process_query(data, sender_ip_port[0], sender_ip_port[1])

#         except Exception as e:
#             print("exception broadcasting ", e)

#     def run(self, start_with_broadcast=True):
#         """
#         "This function is called from the peer.py to start this tracker"
#         ": return: VOID"
#         """
#         threading.Thread(target=self.broadcast_listener).start()
#         if self._is_announce == True:
#             # start the process of pinging.
#             pingMessage = self.ping("aa", "q", r=None)
#             self.broadcast(pingMessage)
#             time.sleep(1)
#             self.printThis("*********************\n\n")

#             findNodeMessage = self.find_node("aa", "q")
#             self.broadcast(findNodeMessage)
#             time.sleep(1)
#             self.printThis("*********************\n\n")

#             getPeerMessage = self.get_peers("aa", "q")
#             self.broadcast(getPeerMessage)
#             time.sleep(1)
#             self.printThis("*********************\n\n")

#             announcePeersMessage = self.announce_peers("aa", "q")
#             self.broadcast(announcePeersMessage)
#             time.sleep(1)

#         else:
#             print("This tracker does not support DHT")
#         """
#         "JUNK YARD!!!!!!!!!"
#         """
#     # def bind_broadcast_socket(self, host='127.0.0.1', DHT_port=5001):
#     #     # self.UDP_broadcast_socket.bind((host, DHT_port))
#     #     # self.UDP_broadcast_socket.setsockopt(
#     #     # socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#     #     print("Tracker is broadcasting at {}:{} ***DHT***".format(host, DHT_port))
#     #     # while True:
#     #     #     data = self.UDP_broadcast_socket.recv(4096)
#     #     #     print("tracker recieved over UDP {}:{}".format(host, DHT_port), data)

#     # def bind_n_listen_response(self, host='127.0.0.1', port=8000):
#     #     self.UDP_response_socket.bind((host, port))
#     #     print("Tracker is accepting responses at {}:{}".format(host, port))
#     #     while True:
#     #         data = self.UDP_response_socket.recv(4096)
#     #         print("tracker recieved over UDP {}:{}".format(host, port), data)
#     #         print("process it now?")

# """
        """
"JUNK YARD!!!!!!!!!"
"""
    # def bind_broadcast_socket(self, host='127.0.0.1', DHT_port=5001):
    #     # self.UDP_broadcast_socket.bind((host, DHT_port))
    #     # self.UDP_broadcast_socket.setsockopt(
    #     # socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    #     print("Tracker is broadcasting at {}:{} ***DHT***".format(host, DHT_port))
    #     # while True:
    #     #     data = self.UDP_broadcast_socket.recv(4096)
    #     #     print("tracker recieved over UDP {}:{}".format(host, DHT_port), data)

    # def bind_n_listen_response(self, host='127.0.0.1', port=8000):
    #     self.UDP_response_socket.bind((host, port))
    #     print("Tracker is accepting responses at {}:{}".format(host, port))
    #     while True:
    #         data = self.UDP_response_socket.recv(4096)
    #         print("tracker recieved over UDP {}:{}".format(host, port), data)
    #         print("process it now?")

"""
