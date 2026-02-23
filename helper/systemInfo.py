import requests
import socket
import platform
import os
from datetime import datetime
import json

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

    def collect_info(self, request) -> dict:
        client_ip = self.get_client_ip(request)
        timestamp = datetime.now().isoformat(timespec="seconds")
        
        # ✅ HTTP HEADERS (Already client data!)
        return {
            "timestamp": timestamp,
            "client_ip": client_ip,
            "client_user_agent": request.headers.get("User-Agent", "unknown"),
            "client_referer": request.headers.get("Referer", "unknown"),
            "client_accept_language": request.headers.get("Accept-Language", "unknown"),
            "client_accept_encoding": request.headers.get("Accept-Encoding", "unknown"),
            "client_host": request.host,
            "request_method": request.method,
            "request_path": request.path,
            "request_query": request.query_string,
            "js_fingerprint_ready": True
        }

