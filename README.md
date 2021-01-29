# P2P Decentralized Network with BitTorrent Protocol

Contributors:

* Ramy Fekry
* Robert Clarkson
* William Lew
* Benjamin Lewis
* John Freirez

# Recording
* file: `screen_recording.mp4`
* link: https://youtu.be/iH-XQL5xXY8

# Project Description:
* This project was an Implementation of a BitTorrent P2P file sharing network protocol. We established connection using a UDP socket between the Trackers, then used TCP sockets to communicate between other Peers to upload and download files. We implemented a file manager to support the uploading and downloading process by arranging fragmented data. The file manager breaks down the file as blocks/pieces of data that's being transferred between peers, then reconstructs the blocks/pieces at the destination. 

Each Peer has a Tracker, Client, Server, Torrent, Message, Downloader, FileManger, and Uploader.

# Libraries Used (To run this program, these libraries must be installed):
* time  ( to slow down the network for debugging )
* shutil  ( to move file to another directory )
* htbps   ( to show the progress bar uploading )
* socket ( to send UDP messages as well as create a persistant connection )
* pickle ( to encode and decode data sent through TCP )
* os ( for file IO )
* threading ( to move processes off the main thread )
* hashlib ( to hash pointers & torrent info )
* bitarray ( to create & modify bitfields )
* uuid ( to generate a unique id for each peer with a low chance of collision )
* bencodepy ( to encode & decode UDP messages )
* math
* builtins

# Python version and compatibility issues:
* Python version 3.8, "anything lower than 3.8 might cause an error" 

# How to run
* To properly test and run you must have two different machines/computers on the same local network.
* Both will have to run `peer.py`, 1 after the other.

```python
python peer.py
```
* please check the video recording:
  * file: `screen_recording.mp4`
  * Link: https://youtu.be/iH-XQL5xXY8

# Challenges 

* Needs multiple machine to properly test, weren't able to test with just one, even tried to use a VM to test but still no luck we needed a different machine.
* While one team member had access to 2 computers, no team member had access to 3 computers. Therefore, the team was unable to test properly with 3 peers connected.
* To complete this project we broke the the project into it's major components and distributed them amongst members.
* BitTorrent implementation was difficult to grasp. Therefore, to make progress the team took a few liberties to implement certain functionalities in their own unique way. While this may break from the BitTorrent protocol it did strengthen each member's grasp of P2P.
