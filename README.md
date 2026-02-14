# Tunnel Session Capture Toolkit

A small Python toolkit for **capturing incoming HTTP request + basic host/environment metadata** via a local Flask endpoint exposed through a tunnel (ngrok/cloudflared/localtunnel). Captured sessions are saved as JSON files under [./session/](cci:9://file:///d:/dsa/custome_tool/session:0:0-0:0).  
Includes a simple **defensive malware scanner** for local folders/drives.

> ⚠️ **Ethics / Safety**
> Use only on systems and traffic you **own** or have **explicit permission** to test. Session logs may contain IP addresses, user-agent strings, and environment details (potentially sensitive).

---

## Use cases

- Debug “who is hitting my endpoint” (IP, headers, path, etc.)
- Capture basic environment metadata during testing (hostname/OS/python version)
- Keep a simple per-client session history in JSON
- Scan local files for suspicious indicators (extensions + string patterns + optional IOC hash list)

---

## Project structure

- [target.py](cci:7://file:///d:/dsa/custome_tool/target.py:0:0-0:0) — Flask app that collects request + system info and stores it in `session/<client_ip>.json`
- [session/](cci:9://file:///d:/dsa/custome_tool/session:0:0-0:0) — stored JSON sessions (each file is a list of captured entries)
- [create_connection.py](cci:7://file:///d:/dsa/custome_tool/create_connection.py:0:0-0:0) — browse stored sessions and (optionally) send one JSON payload to a local listener
- [malware_scanner.py](cci:7://file:///d:/dsa/custome_tool/malware_scanner.py:0:0-0:0) — defensive scanner that produces a CSV report
- [helper/session.py](cci:7://file:///d:/dsa/custome_tool/helper/session.py:0:0-0:0), [helper/systemInfo.py](cci:7://file:///d:/dsa/custome_tool/helper/systemInfo.py:0:0-0:0) — session & data collection helpers
- [main.py](cci:7://file:///d:/dsa/custome_tool/main.py:0:0-0:0) — interactive menu (work in progress / your entrypoint)

---

## Requirements

- Python 3.10+
- Pip / venv recommended

Python packages used (install as needed):
- `flask`
- `pyngrok` (only if you use ngrok via Python)
- `requests` (used by helper code)

Tunnel provider prerequisites (depending on what you use):
- **ngrok**: account + auth token may be required (set via ngrok config)
- **cloudflared**: install `cloudflared` and ensure it is in `PATH`
- **localtunnel**: `npm i -g localtunnel` (command `lt` must be in `PATH`)

---

## Setup

```bash
python -m venv .venv
# Windows PowerShell:
. .\.venv\Scripts\Activate.ps1
# Git Bash:
source .venv/Scripts/activate

pip install flask pyngrok requests