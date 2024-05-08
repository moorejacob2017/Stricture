import os
import psutil
import logging

from time import sleep
from datetime import datetime, time

from .exceptions import *
from .schedule import Schedule
from .stricture import Stricture

class Process:
    def __init__(self, pid):
        type_check_pid(pid)
        self.pid = pid
        self.proc = None

    def launch(self):
        check_pid_exists(self.pid)
        self.proc = psutil.Process(self.pid)

    def resume(self):
        self.proc.resume()

    def pause(self):
        self.proc.suspend()

    def is_alive(self):
        return self.proc.is_running()


class ProcessStricture(Stricture):
    def __init__(
            self,
            pid,
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

        self.process = Process(pid)

        self.set_launch(self.process.launch)
        self.set_resume(self.process.resume)
        self.set_pause(self.process.pause)
        self.set_is_alive(self.process.is_alive)

    def set_pid(self, pid):
        type_check_pid(pid)
        self.pid = pid

    def _execute_func(self, *args, **kwargs):
        logging.info(f'Stricture has been applied')
        
        if not self.is_alive():
            raise StrictureDeadProcess()
        
        try:
            if not self.condition() or not self.schedule.check_schedule():
                self.ex_state = False
                self.pause()
                logging.info(f'Stricture halted pre-running process and is waiting to continue execution')
                while not self.condition() or not self.schedule.check_schedule():
                    sleep(self.sleep_duration)

            while self.is_alive():
                #self.ex_state = self._is_executing()
                # If can execute and not executing
                if (self.condition() and self.schedule.check_schedule()) and not self.ex_state:
                    self.ex_state = True
                    self.resume()
                    logging.info(f'Stricture continuing execution')
                # If can't execute and executing
                elif not (self.condition() and self.schedule.check_schedule()) and self.ex_state:
                    self.ex_state = False
                    self.pause()
                    logging.info(f'Stricture halted execution')
                else:
                    sleep(self.sleep_duration)
            logging.info(f'Process completed execution')
        except KeyboardInterrupt:
            logging.warning(f'Stricture caught KeyboardInterrupt')
            logging.warning(f'Removing stricture from process and continuing execution')
            self.resume()
    def execute(self):
        self.process.launch()
        self._init_functions()
        return self._execute_func(*self._execute_args, **self._execute_kwargs)

