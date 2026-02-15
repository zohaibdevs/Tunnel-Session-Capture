import socket
import threading
import subprocess
import os
import base64
import time

class Helper:
    def __init__(self, conn):
        self.header = 64
        self.formate = 'utf-8'
        self.conn = conn

    def encode(self, message):
        return message.encode(self.formate)

    def decode(self, message):
        return message.decode(self.formate)

    def message(self, message):
        message = self.encode(message)
        msg_length = len(message)
        send_length = self.encode(str(msg_length))
        send_length += b' ' * (self.header - len(send_length))
         
        return {
            "length": send_length,
            "text": message
        }

    def send(self, message):
        message = self.message(message)
        self.conn.send(message['length'])
        self.conn.send(message['text'])

    def msg_length(self):
        message_length = self.receive()
        if message_length:
            return message_length
        return None

    def receive(self, length=64):
        if isinstance(length, str):
            length = int(length)

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
        print("[STARTING] server is starting...")
        self.start()


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

            length = helper.msg_length()
            o = helper.receive(length)
            if o == "exit":
                connected = False
                break
             
            print(f"[Client] {addr}: {o}")
            cmd = input("[Server]?>: ").strip()
            helper.send(cmd)
        conn.close()





class Client():
    def __init__(self, host="0.0.0.0", port=7706):
        self.host = host
        self.port = port
        self.hostname = socket.gethostname()
        self.header = 64
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
                length = helper.msg_length()
                cmd = helper.receive(length)
                if not cmd or cmd == "exit":
                    helper.send("exit")
                    break
                    
                print(f"[server] {self.hostname}: {cmd}")
                
                # Send response back
                helper.send("Command executed")
                
            except Exception as e:
                print(f"Error: {e}")
                break
        self.client.close()





