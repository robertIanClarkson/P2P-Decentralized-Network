from client import Client
from server import Server
from tracker import Tracker
from config import Config
from downloader import downloader

class Peer():
    
    SEEDER = 2;
    LECHES = 1;
    PEER = 0;

    # copy and paste here your code implementation from the peer.py in your Labs
    
    def __init__(self):
        self.role = PEER # default role
        pass
    

