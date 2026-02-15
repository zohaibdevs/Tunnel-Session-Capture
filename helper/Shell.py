import subprocess


class Shell:
    def __init__(self, cmd):
        self.cmd = cmd

    def run(self):
        try:
            # NO PIPES = No deadlock
            result = subprocess.run(self.cmd, shell=True, 
                                  capture_output=True, text=True, timeout=30)
            return {
                'stdout': result.stdout,
                'stderr': result.stderr, 
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {'error': 'Command timeout'}
        except Exception as e:
            return {'error': str(e)}


# term = True
# while term:
#     cmd = input("Enter command: ").strip()
#     if(cmd == "exit"): 
#         print("Shell Closed")
#         term = False
#         break
   
#     shell = Shell(cmd)
#     print(shell.run())
