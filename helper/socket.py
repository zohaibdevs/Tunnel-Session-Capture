import socket
import threading
import subprocess
import os
import time
from .Shell import Shell
import traceback
from typing import Callable

class Helper:
    def __init__(self, conn):
        self.header = 10240
        self.formate = 'utf-8'
        self.conn = conn

    def encode(self, message):
        return message.encode(self.formate)


    def decode(self, message):
        return message.decode(self.formate, errors='ignore')

    def message(self, message):
        message = self.encode(message)
        return message

    def send(self, message):
        message = self.message(message)
        self.conn.send(message)

    def msg_length(self):
        message_length = self.receive().strip()
        if message_length:
            try:
                return int(message_length)
            except (ValueError, TypeError):
                return None
        return None

    def receive(self, length=64):
        return self.decode(self.conn.recv(length))
   



class Server():
    def __init__(self, callback: Callable[[str, Helper], None], host="0.0.0.0", port=7706):
        self.host = host
        self.port = port
        self.hostname = socket.gethostname()
        self.header = 10240
        self.formate = 'utf-8'
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))

        self.start(callback)



    def start(self, callback):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.host}:{self.port}")

        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle, args=(conn, addr, callback))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    def handle(self, conn, addr, callback):
        print(f"[NEW CONNECTION] {addr} connected to the server")

        connected = True
        while connected:
            helper = Helper(conn)

            o = helper.receive(self.header)
            if o == "exit":
                connected = False
                break
            
            callback(o, helper)

        conn.close()





class Client():
    def __init__(self, callback: Callable[[str, Helper], None], host="0.0.0.0", port=7706):
        self.host = host
        self.port = port
        self.hostname = socket.gethostname()
        self.header = 10240
        self.formate = 'utf-8'

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((self.host, self.port))
            helper = Helper(self.client)
            helper.send(f"ALIVE:{socket.gethostname()}")
            callback(helper, self.client)
            print("[CONNECTED] Client connected to server")
        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")
            traceback.print_exc()
            self.client = None
    

    def start(self, callback):
        while True:
            try:
                helper = Helper(self.client)

                cmd = helper.receive(self.header)
               
                if not cmd or cmd == "exit":
                    helper.send("exit")
                    break

                callback(cmd, helper)
            except Exception as e:
                print(f"Error: {e}")
                break
        self.client.close()





