from .exceptions import *

class StrictureFunctionManager:
    def __init__(
            self,
            launch_func=None,
            launch_args=[],
            launch_kwargs={},
            resume_func=None,
            resume_args=[],
            resume_kwargs={},
            pause_func=None,
            pause_args=[],
            pause_kwargs={},
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

        self.was_launch_set = False
        if launch_func:
            self.was_launch_set = True

        self.launch_func=launch_func
        self.launch_args=launch_args
        self.launch_kwargs=launch_kwargs
        self.resume_func=resume_func
        self.resume_args=resume_args
        self.resume_kwargs=resume_kwargs
        self.pause_func=pause_func
        self.pause_args=pause_args
        self.pause_kwargs=pause_kwargs
        self.is_alive_func=is_alive_func
        self.is_alive_args=is_alive_args
        self.is_alive_kwargs=is_alive_kwargs
        self.condition_func=condition_func
        self.condition_args=condition_args
        self.condition_kwargs=condition_kwargs
        self.execute_func=execute_func
        self.execute_args=execute_args
        self.execute_kwargs=execute_kwargs

    def set_launch(self, launch_func=None, launch_args=[], launch_kwargs={}):
        if launch_func:
            self.was_launch_set = True
        if not launch_args == []:
            type_check_array(launch_args)
        if not launch_kwargs == {}:
            type_check_dictionary(launch_kwargs)
        self.launch_args = launch_args
        self.launch_kwargs = launch_kwargs
        if launch_func:
            type_check_function(launch_func)
            self.launch_func = launch_func

    def set_resume(self, resume_func=None, resume_args=[], resume_kwargs={}):
        if not resume_args == []:
            type_check_array(resume_args)
        if not resume_kwargs == {}:
            type_check_dictionary(resume_kwargs)
        self.resume_args = resume_args
        self.resume_kwargs = resume_kwargs
        if resume_func:
            type_check_function(resume_func)
            self.resume_func = resume_func

    def set_pause(self, pause_func=None, pause_args=[], pause_kwargs={}):
        if not pause_args == []:
            type_check_array(pause_args)
        if not pause_kwargs == {}:
            type_check_dictionary(pause_kwargs)
        self.pause_args = pause_args
        self.pause_kwargs = pause_kwargs
        if pause_func:
            type_check_function(pause_func)
            self.pause_func = pause_func

    def set_is_alive(self, is_alive_func=None, is_alive_args=[], is_alive_kwargs={}):
        if not is_alive_args == []:
            type_check_array(is_alive_args)
        if not is_alive_kwargs == {}:
            type_check_dictionary(is_alive_kwargs)
        self.is_alive_args = is_alive_args
        self.is_alive_kwargs = is_alive_kwargs
        if is_alive_func:
            type_check_function(is_alive_func)
            self.is_alive_func = is_alive_func

    def set_condition(self, condition_func=None, condition_args=[], condition_kwargs={}):
        if not condition_args == []:
            type_check_array(condition_args)
        if not condition_kwargs == {}:
            type_check_dictionary(condition_kwargs)
        self.condition_args = condition_args
        self.condition_kwargs = condition_kwargs
        if condition_func:
            type_check_function(condition_func)
            self.condition_func = condition_func

    def set_execute(self, execute_func=None, execute_args=[], execute_kwargs={}):
        if not execute_args == []:
            type_check_array(execute_args)
        if not execute_kwargs == {}:
            type_check_dictionary(execute_kwargs)
        self.execute_args = execute_args
        self.execute_kwargs = execute_kwargs
        if execute_func:
            type_check_function(execute_func)
            self.execute_func = execute_func