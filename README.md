# 🚀 Tunnel Session Capture

Tunnel Session Capture is a Python-based session logging and
communication framework.

It allows you to:

-   Capture client session metadata using a temporary public tunnel
-   Store session data locally in JSON format
-   Establish TCP-based communication (Server / Client mode)
-   Manage sessions interactively via CLI

------------------------------------------------------------------------

## 📁 Project Structure

│ ├── main.py \# CLI entry point ├── app.py \# Flask session capture
server │ ├── helper/ │ ├── C2.py \# Communication wrapper │ ├──
socket.py \# TCP Server & Client implementation │ ├── session.py \#
Session management │ └── systemInfo.py \# System information collection
│ ├── session/ \# Stored session JSON files └── README.md

------------------------------------------------------------------------

# ⚙️ Requirements

-   Python 3.9+
-   pip

Install dependencies:

    pip install flask pyngrok requests

Optional tunnel providers:

Cloudflared: Install from Cloudflare official website.

LocalTunnel: npm install -g localtunnel

------------------------------------------------------------------------

# 🧠 How It Works

1️⃣ Start a capture server using a tunnel provider. 2️⃣ When someone
visits the generated public URL: - Session data is collected. - Data is
saved in the /session directory. - Tunnel closes automatically.

3️⃣ Use main.py to manage sessions and start communication mode.

------------------------------------------------------------------------

# 🔥 Usage Guide

## Step 1 -- Start Main Menu

    python main.py

Menu:

0: Exit\
1: List target sessions\
2: Refresh sessions list\
3: Create new target session

------------------------------------------------------------------------

## Step 2 -- Create New Target Session

Choose option:

    3

Select tunnel provider:

1)  ngrok\
2)  cloudflared\
3)  localtunnel

A public URL will be generated.

When visited → session file saved in:

    /session/<ip>.json

------------------------------------------------------------------------

## Step 3 -- Start Communication

After selecting a session:

Choose IP: 1) Localhost\
2) Public IP\
3) 0.0.0.0

Choose port: 1) Default (7706)\
2) Custom

Choose mode: 1) Listen (Server mode)\
2) Send (Client mode)

------------------------------------------------------------------------

# 📌 Default Ports

Flask Capture: 5000\
Communication: 7706

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
