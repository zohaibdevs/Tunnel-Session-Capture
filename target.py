import argparse
from datetime import datetime
import json
import os
import platform
import shutil
import socket
import subprocess
import threading
from pathlib import Path

from flask import Flask, after_this_request, jsonify, request
from pyngrok import ngrok

app = Flask(__name__)
SESSION_DIR = Path("session")
ACTIVE_TUNNEL = None
ACTIVE_TUNNEL_PROVIDER = "ngrok"
SERVER_PORT = 5000


def get_client_ip() -> str:
    forwarded_for = request.headers.get("X-Forwarded-For", "").strip()
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return (request.remote_addr or "unknown").strip()


def get_local_ip() -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"


def collect_info() -> dict:
    client_ip = get_client_ip()
    local_ip = get_local_ip()
    return {
        "ip": client_ip,
        "local_ip": local_ip,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "client_ip": client_ip,
        "client_user_agent": request.headers.get("User-Agent", "unknown"),
        "client_accept_language": request.headers.get("Accept-Language", "unknown"),
        "client_host": request.host,
        "request_method": request.method,
        "request_path": request.path,
        "server_hostname": socket.gethostname(),
        "server_os": platform.system(),
        "server_os_release": platform.release(),
        "server_os_version": platform.version(),
        "server_machine": platform.machine(),
        "server_processor": platform.processor(),
        "server_python": platform.python_version(),
        "server_working_dir": os.getcwd(),
        "env_username": os.getenv("USERNAME", "unknown"),
        "env_computername": os.getenv("COMPUTERNAME", "unknown"),
        "env_userdomain": os.getenv("USERDOMAIN", "unknown"),
        "env_userprofile": os.getenv("USERPROFILE", "unknown"),
        "env_path": os.getenv("PATH", "unknown"),
    }


def save_session(info: dict) -> Path:
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    safe_ip = info["ip"].replace(":", "_").replace("/", "_") or "unknown"
    output_file = SESSION_DIR / f"{safe_ip}.json"

    sessions: list[dict] = []
    if output_file.exists():
        try:
            with output_file.open("r", encoding="utf-8") as file:
                existing_data = json.load(file)
                if isinstance(existing_data, list):
                    sessions = existing_data
                elif isinstance(existing_data, dict):
                    sessions = [existing_data]
        except Exception:
            sessions = []

    sessions.append(info)

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(sessions, file, indent=2)

    return output_file


def build_session_lines(info: dict, output_file: Path) -> list[str]:
    return [
        f"timestamp: {info['timestamp']}",
        f"client_ip: {info['client_ip']}",
        f"local_ip: {info.get('local_ip', 'unknown')}",
        f"client_user_agent: {info['client_user_agent']}",
        f"client_accept_language: {info['client_accept_language']}",
        f"client_host: {info['client_host']}",
        f"request_method: {info['request_method']}",
        f"request_path: {info['request_path']}",
        f"server_hostname: {info['server_hostname']}",
        f"server_os: {info['server_os']}",
        f"server_os_release: {info['server_os_release']}",
        f"server_os_version: {info['server_os_version']}",
        f"server_machine: {info['server_machine']}",
        f"server_processor: {info['server_processor']}",
        f"server_python: {info['server_python']}",
        f"server_working_dir: {info['server_working_dir']}",
        f"env_username: {info['env_username']}",
        f"env_computername: {info['env_computername']}",
        f"env_userdomain: {info['env_userdomain']}",
        f"env_userprofile: {info['env_userprofile']}",
        f"env_path: {info['env_path']}",
        f"saved_to: {output_file.resolve()}",
    ]


def start_ngrok_tunnel(port: int):
    tunnel = ngrok.connect(port)
    public_url = tunnel.public_url if hasattr(tunnel, "public_url") else str(tunnel)
    return tunnel, public_url


def start_cloudflared_tunnel(port: int):
    cloudflared_bin = shutil.which("cloudflared")
    if not cloudflared_bin:
        raise RuntimeError("cloudflared is not installed or not in PATH.")

    process = subprocess.Popen(
        [
            cloudflared_bin,
            "tunnel",
            "--url",
            f"http://127.0.0.1:{port}",
            "--no-autoupdate",
        ]
    )
    return process, "Cloudflared running (check terminal output for public URL)."


def start_localtunnel_tunnel(port: int):
    localtunnel_bin = shutil.which("lt") or shutil.which("lt.cmd")
    if not localtunnel_bin:
        raise RuntimeError("localtunnel is not installed. Install with: npm i -g localtunnel")

    process = subprocess.Popen([localtunnel_bin, "--port", str(port)])
    return process, "Localtunnel running (check terminal output for public URL)."


def start_tunnel(provider: str, port: int):
    if provider == "ngrok":
        return start_ngrok_tunnel(port)
    if provider == "cloudflared":
        return start_cloudflared_tunnel(port)
    if provider == "localtunnel":
        return start_localtunnel_tunnel(port)
    raise ValueError(f"Unsupported tunnel provider: {provider}")


def close_tunnel() -> None:
    global ACTIVE_TUNNEL
    if ACTIVE_TUNNEL is None:
        return

    if ACTIVE_TUNNEL_PROVIDER == "ngrok":
        try:
            public_url = (
                ACTIVE_TUNNEL.public_url
                if hasattr(ACTIVE_TUNNEL, "public_url")
                else str(ACTIVE_TUNNEL)
            )
            ngrok.disconnect(public_url)
        except Exception as error:
            print(f"[!] Tunnel close error: {error}")
        finally:
            ACTIVE_TUNNEL = None
        return

    try:
        ACTIVE_TUNNEL.terminate()
        ACTIVE_TUNNEL.wait(timeout=3)
    except Exception:
        try:
            ACTIVE_TUNNEL.kill()
        except Exception as error:
            print(f"[!] Tunnel process close error: {error}")
    finally:
        ACTIVE_TUNNEL = None


def shutdown_server() -> bool:
    shutdown = request.environ.get("werkzeug.server.shutdown")
    if shutdown is None:
        print("[!] Server shutdown hook not available.")
        return False
    shutdown()
    return True


def force_exit() -> None:
    os._exit(0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start target server with selected tunnel provider")
    parser.add_argument(
        "--tunnel",
        choices=["ngrok", "cloudflared", "localtunnel"],
        default="ngrok",
        help="Tunnel provider to expose local Flask app",
    )
    return parser.parse_args()


@app.route("/")
def home():
    target = collect_info()
    output_file = save_session(target)
    payload = {
        "target": target,
        "saved_to": str(output_file.resolve()),
    }

    print("\n[+] New session captured")
    print(json.dumps(payload, indent=2))

    @after_this_request
    def close_after_response(response):
        close_tunnel()
        did_shutdown = shutdown_server()
        if not did_shutdown:
            threading.Timer(1.0, force_exit).start()
        print("[*] Tunnel closed and server stopped after session capture.")
        return response

    return jsonify(payload)


if __name__ == "__main__":
    args = parse_args()
    ACTIVE_TUNNEL_PROVIDER = args.tunnel

    try:
        ACTIVE_TUNNEL, public_url = start_tunnel(args.tunnel, SERVER_PORT)
    except Exception as error:
        raise SystemExit(f"Failed to start {args.tunnel} tunnel: {error}")

    print(f"Tunnel provider: {args.tunnel}")
    print(f"Public URL: {public_url}")
    print(f"Forwarding to: http://127.0.0.1:{SERVER_PORT}")

    app.run(host="0.0.0.0", port=SERVER_PORT, use_reloader=False, threaded=False)
