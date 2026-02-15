
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
first of all if we need to use server & client before that we need to create session with target machine I will mention below how thing work.
 
- How To Create Session
- How to start server
- How to start client

## Menu

    root@terminal> python main.py
    0: exit
    1: List target sessions
    2. Refresh session list
    3. create new target session


## How To Create Session
First we need to create session wit target machine

### Step 1 --  Select Tunnel Provider (Select 3 from menu)

    Select tunnel provider:
    1: ngrok
    2: cloudflared
    3. localtunnel
### Step 2 -- Public URL
send public URL to target machine for capturing the info into session. when target machine open the URL into browser after getting there session info server automatically close 

find this to in terminal 

    public: url
    your url is: url

## How To Start Server
Start Listening server on our just send message to client and get response back

###  Step 1 -- Select 1 to Get List of Session
I am displaying local IP due to security purpose  don't worry session list show the public IP instead of local IP

    [1] 192.168.0.0
    [2] 192.168.0.7
    [3] 192.168.0.8
    etc....
    pick session number: you can add by number example 1
    

### Step 2 -- After Selecting Session from list  

    Select Ip Option:
    0: exit
    1: Localhost (192.168.0.7)
    2: Public IP (**.***.***.165)
    3: Use IP 0.0.0.0
    Enter Ip Option: 1
    
### Step 3 -- Select Port Right after Ip Selection
Select The Port of target machine

    0: Exit
    1: Use Default Port (7706)
    2: Use Custom Port (If you want any port number)
    Enter Port Option: 1

### Step 4 -- Start Server/Client
You can run server / client By Chosing one of theme option 

    0: Exit
    1: Start Server
    2: Start Client
    Enter C2 Option: 1

### On Serve Start
Now Server is waiting for client 

    [*] Starting SERVER on 192.168.1.7:7706
    [STARTING] server is starting...
    [LISTENING] Server is listening on 192.168.1.7:7706

### On Client Start

	[*] Starting CLIENT to 192.168.1.7:7706
	[STARTING] client is starting...
	[CONNECTED] Client connected to server
  
  ### After Client Started Server Auto Capture the Connection

	[NEW CONNECTION] ('192.168.1.7', port_number) connected to the server
	[ACTIVE CONNECTIONS] 1
	[Client] ('192.168.0.0', port_number): ALIVE:DESKTOP-PML7EU0
	[Server]?>: 
  
    

------------------------------------------------------------------------

# 🛡 Disclaimer

This project is intended for educational and internal communication
testing purposes only.

The author is not responsible for misuse.

------------------------------------------------------------------------

# 👨‍💻 Author

Zohaib Ud Din\
GitHub: https://github.com/zohaibdevs/Tunnel-Session-Capture.git

------------------------------------------------------------------------

# 📜 License

MIT License