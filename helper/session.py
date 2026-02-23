from .systemInfo import SystemInfo
from pathlib import Path
import json


class Session(SystemInfo):
    def __init__(self):
        super().__init__()   # ✅ important
        self.session_dir = Path("session")
        self.sessions = {}

    def getSessions(self):
        if not self.session_dir.is_dir():
            return {}
        
        sessions = [f for f in self.session_dir.glob("*.json") if f.is_file()]

        
        if(len(sessions) == 0):
            return None
        
        for index, session in enumerate(sessions):
            self.sessions[index + 1] = session
            print(f"[{index + 1}] {session.name}")
    
        return self.sessions
    

    def getSession(self, session_id):
        if session_id not in self.sessions:
            return None
        return self.sessions[session_id]

    def loadSession(self, session_id):
        session = self.getSession(int(session_id))
        if session is None:
            return None
        return self.load_json(session)

    def createSession(self, session_id, request):
        session = self.collect_info(request)
        if session is None:
            return None
        return self.save_session(session)

    def save_session(self, session):
        self.session_dir.mkdir(parents=True, exist_ok=True)
        safe_ip = session["client_ip"].replace(":", "_").replace("/", "_") or "unknown"
        output_file = self.session_dir / f"{safe_ip}.json"

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

        sessions.append(session)

        with output_file.open("w", encoding="utf-8") as file:
            json.dump(sessions, file, indent=2)

        return output_file

    def load_json(self, path: str):
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)