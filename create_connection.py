import json
import os
import socket


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def pick_target(session_data: object) -> dict:
    if isinstance(session_data, list):
        if not session_data:
            raise ValueError("Session file has no entries")
        last_entry = session_data[-1]
        if not isinstance(last_entry, dict):
            raise ValueError("Invalid session entry format")
        target = last_entry
        if "ip" not in target and "client_ip" in target:
            target["ip"] = target.get("client_ip")
        if "local_ip" not in target:
            target["local_ip"] = "unknown"
        return target

    if isinstance(session_data, dict):
        target = session_data.get("target", session_data)
        if not isinstance(target, dict):
            raise ValueError("Invalid target format")
        if "ip" not in target and "client_ip" in target:
            target["ip"] = target.get("client_ip")
        if "local_ip" not in target:
            target["local_ip"] = "unknown"
        return target

    raise ValueError("Unsupported session JSON type")


def send_target_to_local_listener(selected_target: dict, host: str = "127.0.0.1", port: int = 4444) -> None:
    payload = json.dumps(selected_target) + "\n"
    data = payload.encode("utf-8")

    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            sock.sendall(data)
    except Exception as error:
        raise RuntimeError(f"Failed to connect/send to {host}:{port} -> {error}")


def main() -> None:
    session_dir = "session"
    if not os.path.isdir(session_dir):
        raise SystemExit("No session folder found yet.")

    sessions = sorted([name for name in os.listdir(session_dir) if name.endswith(".json")])
    if not sessions:
        raise SystemExit("No JSON sessions found.")

    print("List of existing sessions:")
    for index, name in enumerate(sessions, 1):
        print(f"[{index}] {name}")

    selected = int(input("Pick session number: ").strip())
    if selected < 1 or selected > len(sessions):
        raise SystemExit("Invalid session number.")

    selected_file = sessions[selected - 1]
    selected_path = os.path.join(session_dir, selected_file)
    print(f"\nSelected session: {selected_file}")

    try:
        session_data = load_json(selected_path)
    except json.JSONDecodeError as error:
        raise SystemExit(f"Invalid JSON in session file: {selected_file}\n{error}")

    selected_target = pick_target(session_data)

    print("\nTarget JSON (you can use selected_target['ip']):")
    print(json.dumps(selected_target, indent=2))
    print("\nQuick access:")
    print(f"selected_target['ip'] = {selected_target.get('ip', 'unknown')}")
    print(f"selected_target['local_ip'] = {selected_target.get('local_ip', 'unknown')}")

    send_choice = input("\nSend this target JSON to a LOCAL listener on 127.0.0.1:4444? (y/n): ").strip().lower()
    if send_choice == "y":
        try:
            send_target_to_local_listener(selected_target, host="127.0.0.1", port=4444)
            print("[+] Sent selected_target JSON to 127.0.0.1:4444")
        except Exception as error:
            print(f"[!] {error}")


if __name__ == "__main__":
    main()
