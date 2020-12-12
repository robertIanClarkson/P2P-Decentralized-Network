from builtins import object
import socket
from threading import Thread

# Robert's Server from TCP Project
class Server(object):
    MAX_NUM_CONN = 10

    def __init__(self, ip_address='127.0.0.1', port=13000):
        # save ip & host
        self.host = ip_address
        self.port = port

        # create an INET, STREAMing socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # server state
        self.clients = {}  # key: client_id, value: clientHandler
        self.names = {}  # key: client_id, value: client_name
        self.rooms = {}  # key: room_number, value: [client_id]

    def _bind(self):
        self.serversocket.bind((self.host, self.port))

    def _listen(self):
        self.serversocket.listen(self.MAX_NUM_CONN)
        print("(S) Server listening at {host}/{port}".format(host=self.host, port=self.port))

    def _accept_clients(self):
        while True:
            # accept the new client
            clienthandler, addr = self.serversocket.accept()

            # start a new thread
            Thread(target=self.client_handler_thread, args=(clienthandler, addr), daemon=True).start()

    # main thread entry point
    def client_handler_thread(self, clientsocket, address):
        print("(S) Just threaded a new client")
        # create the client handler
        # client_handler = ClientHandler(self, clientsocket, address)

        # # init the CH
        # client_handler.init()

        # try:
        #     # run the main logic
        #     client_handler.run()
        # except EOFError as err:
        #     client_id = client_handler.client_id
        #     print("(x) Client Handler Thread Error --> Client ({name}:{client_id}) left abruptly".format(name=self.names[client_id], client_id=client_id))
        #     client_handler.delete_client_data()
        # except Exception as err:
        #     print("(x) Client Handler Thread Error --> {err}".format(err=err))
        #     client_handler.delete_client_data()

    # main server logic
    def run(self):
        self._bind()
        self._listen()
        self._accept_clients()

# if __name__ == '__main__':
#     try:
#         server = Server()
#         server.run()
#     except Exception as err:
#         print("(x) Server Error --> {err}".format(err=err))
