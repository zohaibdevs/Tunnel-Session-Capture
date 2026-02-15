import socket
import base64
import subprocess
import threading
import time
import sys
from .socket import Server, Client

class C2Server():
    def __init__(self, host="0.0.0.0", port=7706):
        self.host = host
        self.port = int(port)

    def start_server(self):
        print("[STARTING] server is starting...")
        self.server = Server(self.host, self.port)
        self.server.start()

    def start_client(self):
        print("[STARTING] client is starting...")
        self.client = Client(self.host, self.port)
        self.client.start()
   