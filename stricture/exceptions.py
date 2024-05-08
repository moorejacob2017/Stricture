import os
import psutil
import json
import types


from .schedule import Schedule


class StrictureBlankResume(Exception):
    def __init__(self):
        super().__init__("Stricture Class must be provided with a start function")
class StrictureBlankPause(Exception):
    def __init__(self):
        super().__init__("Stricture Class must be provided with a stop function")
class StrictureBlankIsAlive(Exception):
    def __init__(self):
        super().__init__("Stricture Class must be provided with an is_alive function")
class StrictureDeadProcess(Exception):
    def __init__(self):
        super().__init__("Stricture recipient process not found alive during initial execution")


def type_check_schedule(variable):
    if not isinstance(variable, (Schedule, dict)):
        try:
            json.loads(variable) # Check if the variable is JSON-parseable
        except (TypeError, ValueError):
            raise TypeError(f"Expected a Scheduler class, dictionary, or JSON, but got {type(variable).__name__}")
def type_check_function(variable):
    if not callable(variable):
        raise TypeError(f"Expected a function/method, but got {type(variable).__name__}")
def type_check_int(variable):
    if not isinstance(variable, int):
        raise TypeError(f"Expected an int, but got {type(variable).__name__}")
def type_check_array(variable):
    if not isinstance(variable, (list, tuple, set, frozenset, range)):
        raise TypeError(f"Expected an array-like object, but got {type(variable).__name__}")
def type_check_dictionary(variable):
    if not isinstance(variable, dict):
        raise TypeError(f"Expected a dictionary, but got {type(variable).__name__}")
def type_check_pid(variable):
    if not isinstance(variable, int):
        if not (isinstance(variable, str) and variable.isdigit()): # v---- can say string if it's a string but not digits
            raise TypeError(f"Expected an int or a numerical string, but got {type(variable).__name__}")


def check_pid_exists(pid):
    if not psutil.pid_exists(pid):
        raise psutil.NoSuchProcess(pid)
    return True

# Only a warning
def check_user(pid):
    # Return false when users are not a match and not root
    process = psutil.Process(pid)
    process_euid = process.uids().effective
    current_euid = os.geteuid()

    if process_euid == current_euid or current_euid == 0:
        return True
    else:
        return False
    
def is_json(variable):
    try:
        json.loads(variable)
        return True
    except (TypeError, ValueError):
        return False


