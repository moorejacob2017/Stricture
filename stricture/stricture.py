import logging

from .exceptions import *
from .schedule import Schedule
from .sfm import StrictureFunctionManager

from time import sleep
from datetime import datetime, time


class Stricture:
    def __init__(
            self,
            schedule=None,
            sleep_duration=10,
            launch_func=None,
            launch_args=[],
            launch_kwargs={},
            pause_func=None,
            pause_args=[],
            pause_kwargs={},
            resume_func=None,
            resume_args=[],
            resume_kwargs={},
            is_alive_func=None,
            is_alive_args=[],
            is_alive_kwargs={},
            condition_func=None,
            condition_args=[],
            condition_kwargs={},
            execute_func=None, 
            execute_args=[],
            execute_kwargs={},
        ):

        self.funcs = StrictureFunctionManager(
            launch_func,
            launch_args,
            launch_kwargs,
            resume_func,
            resume_args,
            resume_kwargs,
            pause_func,
            pause_args,
            pause_kwargs,
            is_alive_func,
            is_alive_args,
            is_alive_kwargs,
            condition_func,
            condition_args,
            condition_kwargs,
            execute_func,
            execute_args,
            execute_kwargs,
        )

        type_check_int(sleep_duration)
        self.sleep_duration = sleep_duration
        
        self.ex_state = True

        if schedule:
            self.set_schedule(schedule)
        else:
            self.schedule = Schedule()

    def _init_functions(self):
        self._launch_args = self.funcs.launch_args
        self._launch_kwargs = self.funcs.launch_kwargs
        self._resume_args = self.funcs.resume_args
        self._resume_kwargs = self.funcs.resume_kwargs
        self._pause_args = self.funcs.pause_args
        self._pause_kwargs = self.funcs.pause_kwargs
        self._is_alive_args = self.funcs.is_alive_args
        self._is_alive_kwargs = self.funcs.is_alive_kwargs
        self._condition_args = self.funcs.condition_args
        self._condition_kwargs = self.funcs.condition_kwargs
        self._execute_args = self.funcs.execute_args
        self._execute_kwargs = self.funcs.execute_kwargs

        if not self.funcs.resume_func:
            raise StrictureBlankResume()
        if not self.funcs.pause_func:
            raise StrictureBlankPause()
        if not self.funcs.is_alive_func:
            raise StrictureBlankIsAlive()
        
        if self.funcs.launch_func:
            self._launch_func = self.funcs.launch_func
        if self.funcs.resume_func:
            self._resume_func = self.funcs.resume_func
        if self.funcs.pause_func:
            self._pause_func = self.funcs.pause_func
        if self.funcs.is_alive_func:
            self._is_alive_func = self.funcs.is_alive_func
        if self.funcs.condition_func:
            self._condition_func = self.funcs.condition_func
        if self.funcs.execute_func:
            self._execute_func = self.funcs.execute_func

    def set_schedule(self, schedule):
        type_check_schedule(schedule)
        if isinstance(schedule, dict):
            self.schedule = Schedule.from_dict(schedule)
        elif is_json(schedule):
            self.schedule = Schedule.from_json(schedule)
        else:
            self.schedule = schedule

    def _launch_func(self, *args, **kwargs):
        pass
    def launch(self):
        return self._launch_func(*self._launch_args, **self._launch_kwargs)
    def set_launch(self, launch_func=None, launch_args=[], launch_kwargs={}):
        self.funcs.set_launch(launch_func, launch_args, launch_kwargs)

    def _resume_func(self, *args, **kwargs):
        pass
    def resume(self):
        return self._resume_func(*self._resume_args, **self._resume_kwargs)
    def set_resume(self, resume_func=None, resume_args=[], resume_kwargs={}):
        self.funcs.set_resume(resume_func, resume_args, resume_kwargs)

    def _pause_func(self, *args, **kwargs):
        pass
    def pause(self):
        return self._pause_func(*self._pause_args, **self._pause_kwargs)
    def set_pause(self, pause_func=None, pause_args=[], pause_kwargs={}):
        self.funcs.set_pause(pause_func, pause_args, pause_kwargs)

    def _is_alive_func(self, *args, **kwargs):
        pass
    def is_alive(self):
        return self._is_alive_func(*self._is_alive_args, **self._is_alive_kwargs)
    def set_is_alive(self, is_alive_func=None, is_alive_args=[], is_alive_kwargs={}):
        self.funcs.set_is_alive(is_alive_func, is_alive_args, is_alive_kwargs)

    def _condition_func(self, *args, **kwargs):
        return True
    def condition(self):
        return self._condition_func(*self._condition_args, **self._condition_kwargs)
    def set_condition(self, condition_func=None, condition_args=[], condition_kwargs={}):
        self.funcs.set_condition(condition_func, condition_args, condition_kwargs)


    def _execute_func(self, *args, **kwargs):
        logging.info(f'Stricture has been applied')

        # Initial Check if already running
        if self.funcs.was_launch_set:
            self.ex_state = False
            if not self.condition() or not self.schedule.check_schedule():
                # Wait to launch
                logging.info(f'Stricture waiting to launch')
                while not self.condition() or not self.schedule.check_schedule():
                    sleep(self.sleep_duration)
            self.ex_state = True
            self.launch()
            logging.info(f'Stricture launched')
            #sleep(10)

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
        self._init_functions()
        return self._execute_func(*self._execute_args, **self._execute_kwargs)
    def set_execute(self, execute_func=None, execute_args=[], execute_kwargs={}):
        self.funcs.set_execute(execute_func, execute_args, execute_kwargs)



