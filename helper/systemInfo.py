import requests
import socket
import platform
import os
from datetime import datetime


class SystemInfo: 
    def __init__(self):
        self.info = {}

    def getSystemInfo(self):
        return self.info
    
    def get_client_ip(self, request):
        forwarded_for = request.headers.get("X-Forwarded-For", "").strip()
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return (request.remote_addr or "unknown").strip()

    def get_local_ip(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.connect(("8.8.8.8", 80))
                return sock.getsockname()[0]
        except Exception:
            try:
                return socket.gethostbyname(socket.gethostname())
            except Exception:
                return "127.0.0.1"

    
    def collect_info(self, request) -> dict:
        client_ip = self.get_client_ip(request)
        local_ip = self.get_local_ip()
        timestamp = datetime.now().isoformat(timespec="seconds")
        return {
            "ip": client_ip,
            "local_ip": local_ip,
            "timestamp": timestamp,
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
