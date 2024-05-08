import os
import errno
import fcntl
import shlex
import signal
import json
import subprocess
from time import sleep
from datetime import datetime, time

from .exceptions import *
from .schedule import Schedule
from .stricture import Stricture


def type_check_str(variable):
    if not isinstance(variable, str):
        raise TypeError(f"Expected an str, but got {type(variable).__name__}")

def set_fd_nonblocking(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

def read_nonblocking(fd, block_size):
    try:
        return os.read(fd.fileno(), block_size)
    except OSError as e:
        if e.errno != errno.EAGAIN:
            raise
        return b''

class Command:
    def __init__(self, command):
        type_check_str(command)
        self.command = command

        self.started_at = 0
        self.finished_at = 0
        self.stdout = ''
        self.stderr = ''

        self.executed = False
        self._proc = None

    def __str__(self):
        return self.to_str()

    def _launch(self):
        self.started_at = int(datetime.now().timestamp()) # Epoch Time
        self._proc = subprocess.Popen(
            shlex.split(self.command),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        set_fd_nonblocking(self._proc.stdout)
        set_fd_nonblocking(self._proc.stderr)

    def _resume(self):
        self._proc.send_signal(signal.SIGCONT)

    def _pause(self):
        self._proc.send_signal(signal.SIGSTOP)

    def _is_alive(self):
        self._no_check_read()
        if not self.executed:
            self._proc.poll()
            if self._proc.returncode is None:
                return True
            else:
                self.executed = True
                self.finished_at = int(datetime.now().timestamp()) # Epoch Time
                return False
            
    def _no_check_read(self):
        BLOCK_SIZE = 131072
        stdout_data = read_nonblocking(self._proc.stdout, BLOCK_SIZE)
        stderr_data = read_nonblocking(self._proc.stderr, BLOCK_SIZE)

        if stdout_data:
            self.stdout += stdout_data.decode('utf-8', 'ignore')
        if stderr_data:
            self.stderr += stderr_data.decode('utf-8', 'ignore')

    def _read(self):
        # BLOCK_SIZE: Size of read buffer in to memory
        # The larger this is, the faster the command runs ?????
        #BLOCK_SIZE = 1048576
        BLOCK_SIZE = 131072
        
        if self._is_alive():
            stdout_data = read_nonblocking(self._proc.stdout, BLOCK_SIZE)
            stderr_data = read_nonblocking(self._proc.stderr, BLOCK_SIZE)
            #print(stdout_data)
            if stdout_data:
                self.stdout += stdout_data.decode('utf-8', 'ignore')
            if stderr_data:
                self.stderr += stderr_data.decode('utf-8', 'ignore')
        else:
            while True:
                stdout_data = read_nonblocking(self._proc.stdout, BLOCK_SIZE)
                stderr_data = read_nonblocking(self._proc.stderr, BLOCK_SIZE)

                if not stdout_data and not stderr_data:
                    break

                if stdout_data:
                    self.stdout += stdout_data.decode('utf-8', 'ignore')

                if stderr_data:
                    self.stderr += stderr_data.decode('utf-8', 'ignore')

    def _wait(self):
        while self._is_alive():
            self._read()
            sleep(1)
        self._read()

    def run(self):
        self.executed = False
        self._launch()
        self._wait()

    def to_dict(self):
        d = {
            "command": self.command,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "stdout": self.stdout,
            "stderr": self.stderr,
        }
        return d
    
    def to_json(self):
        d = {
            "command": self.command,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "stdout": self.stdout,
            "stderr": self.stderr,
        }
        return d
    
    def to_str(self):
        d = {
            "command": self.command,
            "started_at": datetime.fromtimestamp(self.started_at).strftime("%Y-%m-%d %H:%M:%S"),
            "finished_at": datetime.fromtimestamp(self.finished_at).strftime("%Y-%m-%d %H:%M:%S"),
            "stdout": self.stdout,
            "stderr": self.stderr,
        }
        return json.dumps(d, indent=4)

class CommandStricture(Stricture):
    def __init__(
            self,
            command,
            schedule=None,
            sleep_duration=10,
            condition_func=None,
            condition_args=[],
            condition_kwargs={},
        ):

        super().__init__(
            schedule=schedule,
            sleep_duration=sleep_duration,
            condition_func=condition_func,
            condition_args=condition_args,
            condition_kwargs=condition_kwargs,
        )

        self.bash_command = Command(cmd)

        self.set_launch(self.bash_command._launch)
        self.set_resume(self.bash_command._resume)
        self.set_pause(self.bash_command._pause)
        self.set_is_alive(self.bash_command._is_alive)

    def execute(self):
        self._init_functions()
        self._execute_func(*self._execute_args, **self._execute_kwargs)
        self.bash_command._read()
        return self.bash_command
