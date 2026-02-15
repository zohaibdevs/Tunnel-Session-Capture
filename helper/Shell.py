import subprocess


class Shell:
    def __init__(self, cmd):
        self.cmd = cmd

    def run(self):
        try:
            proc = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output = proc.stdout.read() + proc.stderr.read()
            return output
        except Exception as e:
            return str(e)