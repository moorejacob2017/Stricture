# `Stricture` Class
- [About](#about)
- [Logging](#logging)
- [Abstract Method Behaviors & Requirements](#abstract-method-behaviors--requirements)
  - [`launch` (Optional)](#launch-optional)
  - [`pause` (Required)](#pause-required)
  - [`resume` (Required)](#resume-required)
  - [`is_alive` (Required)](#is_alive-required)
  - [`condition` (Optional)](#condition-optional)
  - [`execute` (Optional)](#execute-optional)
- [Instantiation](#instantiation)
  - [Instantiation Example](#instantiation-example)
  - [`schedule: stricture.Schedule`](#schedule-strictureschedule)
  - [`sleep_duration: int`](#sleep_duration-int)
  - [`launch_func: function`](#launch_func-function)
  - [`launch_args: list[*]`](#launch_args-list)
  - [`launch_kwargs: dict{str,*}`](#launch_kwargs-dictstr)
  - [`pause_func: function`](#pause_func-function)
  - [`pause_args: list[*]`](#pause_args-list)
  - [`pause_kwargs: dict{str,*}`](#pause_kwargs-dictstr)
  - [`resume_func: function`](#resume_func-function)
  - [`resume_args: list[*]`](#resume_args-list)
  - [`resume_kwargs: dict{str,*}`](#resume_kwargs-dictstr)
  - [`is_alive_func: function`](#is_alive_func-function)
  - [`is_alive_args: list[*]`](#is_alive_args-list)
  - [`is_alive_kwargs: dict{str,*}`](#is_alive_kwargs-dictstr)
  - [`condition_func: function`](#condition_func-function)
  - [`condition_args: list[*]`](#condition_args-list)
  - [`condition_kwargs: dict{str,*}`](#condition_kwargs-dictstr)
  - [`execute_func: function`](#execute_func-function)
  - [`execute_args: list[*]`](#execute_args-list)
  - [`execute_kwargs: dict{str,*}`](#execute_kwargs-dictstr)
- [Methods](#methods)
  - [`set_schedule`](#set_schedule)
  - [`set_launch`](#set_launch)
  - [`set_pause`](#set_pause)
  - [`set_resume`](#set_resume)
  - [`set_is_alive`](#set_is_alive)
  - [`set_condition`](#set_condition)
  - [`set_execute`](#set_execute)
  - [`execute`](#execute)

## About
The `Stricture` class abstracts process management (process in its generic definition). It generalizes the series of steps for launching a process, checking a condition, checking a schedule, pausing the process based on condition/schedule, and resuming the process based on condition/schedule, until the process is completed. This is done by defining a `Schedule` object and 5 abstract methods; `launch`, `pause`, `resume`, `is_alive`, and `condition`. The schedule and methods are then given to a 6th templated method, `execute`, that coordinates their usage for the desired effect.

These 5 methods can be set by the package user for interacting with various appliances. For example a `Stricture` can be used to start and stop a process on an API or it can be used to send SIGSTOPs and SIGCONTs to local Linux processes. 

Defining the behavior of the these methods can be done by either providing the appropriate arguments during instantiation, or by using the provided setter methods; `set_launch`, `set_pause`, `set_resume`, `set_is_alive`, and `set_condition`. The instantiation arguments and setter methods take python functions to use in the `execute` template, and the function args and kwargs they should be executed with.

__WARNING:__ Manually monkey patching and modifying `Stricture` attributes is not recommended. Doing so is liable to cause unintended functionality and bugs. Use the provided methods for setting and interacting with the `Stricture` class.

For a demo of a `Stricture` being used to interact with an API, please see [Example.md](../example/Example.md).

##### Basic API Example
```python
import stricture
import requests
from .dummy_manager import DummyAPIManager

# Run a process on an API
# Run the process from 7:00am-7:00pm on weekdays
# Pause the process at any other time
# Pause the process on weekends
# Require that a specific url be reached to continue execution (my_condition)

def my_condition(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False

def main():
    # Example API Manager
    # Provides Functions...
    #   api_launch() - starts a process on the api
    #   api_pause() - pauses the process on the api
    #   api_resume() - resumes the process on the api
    #   api_is_alive() - checks if the process on the api is still running
    dummy = DummyAPIManager('http://127.0.0.1:5000/')
    
    # Schedule:
    #   7:00am-7:00pm on weekdays
    #   Never on weekends
    schedule_dict = {
        'start_time':'7:00',
        'stop_time':'19:00',
        'prohibited_days':[
            'Saturday',
            'Sunday'
        ]
    }

    # Initialize as Schedule from a Dict
    my_schedule = stricture.Schedule.from_dict(schedule_dict)

    dummy_stricture = stricture.Stricture(my_schedule) # Initialize Stricture with schedule
    dummy_stricture.set_launch(dummy.api_launch) # Set how to launch the process
    dummy_stricture.set_pause(dummy.api_pause) # Set how to pause the process
    dummy_stricture.set_resume(dummy.api_resume) # Set how to resume the process
    dummy_stricture.set_is_alive(dummy.api_is_alive) # Set how to check if process is alive or completed
    dummy_stricture.set_condition(
        condition_func=my_condition,
        condition_args=['https://example.com/']
    ) # Set the function to check if condition is met

    dummy_stricture.execute() # Runs the process according to the schedule

    print('Done!')

if __name__ == "__main__":
    main()
```


## Logging
`Stricture` classes provide basic logging, but not by default. One can monitor stricture execution by including the following in their script:
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %Z'
)
```

## Abstract Method Behaviors & Requirements


### `launch` (Optional)
- A function for starting a process for the very first time. 
- Is optional.
- When left undefined, assumes that the process has already been launched. 
- If the process is not found to be running during initial execution, a `StrictureDeadProcess` Exception will be raised. 
- Does not require anything to be returned. 
- Can be set via `Stricture` instantiation with `launch_func`, `launch_args`, and `launch_kwargs`.
- Can be set by using `set_launch` with `launch_func`, `launch_args`, and `launch_kwargs`.

### `pause` (Required)
- A function for stopping a running process.
- Is required.
- When left undefined, raises a `StrictureBlankPause` Exception upon the call to `execute`. 
- Does not require anything to be returned. 
- Can be set via `Stricture` instantiation with `pause_func`, `pause_args`, and `pause_kwargs`.
- Can be set by using `set_pause` with `pause_func`, `pause_args`, and `pause_kwargs`.

### `resume` (Required)
- A function for continuing a stopped process.
- Is required. 
- When left undefined, raises a `StrictureBlankResume` Exception upon the call to `execute`.
- Does not require anything to be returned. 
- Can be set via `Stricture` instantiation with `resume_func`, `resume_args`, and `resume_kwargs`.
- Can be set by using `set_resume` with `resume_func`, `resume_args`, and `resume_kwargs`.

### `is_alive` (Required)
- A function for checking if the process has completed.
- Is required. 
- When left undefined, raises a `StrictureBlankIsAlive` Exception upon the call to `execute`.
- Requires a `bool` to be returned.
- Must return `True` if the process is still running.
- Must return `False` if the process has completed.
- Can be set via `Stricture` instantiation with `is_alive_func`, `is_alive_args`, and `is_alive_kwargs`.
- Can be set by using `set_is_alive` with `is_alive_func`, `is_alive_args`, and `is_alive_kwargs`.

### `condition` (Optional)
- A function for defining any other conditions or requirements that should dictate when a process is launched, paused, or resumed. 
- Is optional.
- When left undefined, always returns `True` and has no affect on execution.
- Requires a `bool` to be returned. 
- Must return `True` if the desired conditions are met.
- Must return `False` if the desired conditions are unsatisfied. 
- Can be set via `Stricture` instantiation with `condition_func`, `condition_args`, and `condition_kwargs`.
- Can be set by using `set_condition` with `condition_func`, `condition_args`, and `condition_kwargs`.

### `execute` (Optional)
__WARNING:__ Setting the `execute` function is __not__ recommended for general usage. However, changing the execution flow may be desired in some rare situations. Therefore, the option to change the default functionality has been left to the users. Modify at your own risk.
- A function that handles all abstracted function calls, condition checks, and the execution flow of the `Stricture` class (the main "body" of the class).
- Wraps all prior abstracted methods into a templated function. 
- Is not recommended to modify.
- Can be set via `Stricture` instantiation with `execute_func`, `execute_args`, and `execute_kwargs`.
- Can be set by using `set_execute` with `execute_func`, `execute_args`, and `execute_kwargs`.

## Instantiation
- [Instantiation Example](#instantiation-example)
  - [`schedule: stricture.Schedule`](#schedule-strictureschedule)
  - [`sleep_duration: int`](#sleep_duration-int)
  - [`launch_func: function`](#launch_func-function)
  - [`launch_args: list[*]`](#launch_args-list)
  - [`launch_kwargs: dict{str,*}`](#launch_kwargs-dictstr)
  - [`pause_func: function`](#pause_func-function)
  - [`pause_args: list[*]`](#pause_args-list)
  - [`pause_kwargs: dict{str,*}`](#pause_kwargs-dictstr)
  - [`resume_func: function`](#resume_func-function)
  - [`resume_args: list[*]`](#resume_args-list)
  - [`resume_kwargs: dict{str,*}`](#resume_kwargs-dictstr)
  - [`is_alive_func: function`](#is_alive_func-function)
  - [`is_alive_args: list[*]`](#is_alive_args-list)
  - [`is_alive_kwargs: dict{str,*}`](#is_alive_kwargs-dictstr)
  - [`condition_func: function`](#condition_func-function)
  - [`condition_args: list[*]`](#condition_args-list)
  - [`condition_kwargs: dict{str,*}`](#condition_kwargs-dictstr)
  - [`execute_func: function`](#execute_func-function)
  - [`execute_args: list[*]`](#execute_args-list)
  - [`execute_kwargs: dict{str,*}`](#execute_kwargs-dictstr)


### Instantiation Example
```python
import stricture
import requests
from .dummy_manager import DummyAPIManager

# Run a process on an API
# Run the process from 7:00am-7:00pm on weekdays
# Pause the process at any other time
# Pause the process on weekends
# Require that a specific url be reached to continue execution (my_condition)

def my_condition(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False

def main():
    # Example API Manager
    # Provides Functions...
    #   api_launch() - starts a process on the api
    #   api_pause() - pauses the process on the api
    #   api_resume() - resumes the process on the api
    #   api_is_alive() - checks if the process on the api is still running
    dummy = DummyAPIManager('http://127.0.0.1:5000/')
    
    # Schedule:
    #   7:00am-7:00pm on weekdays
    #   Never on weekends
    schedule_dict = {
        'start_time':'7:00',
        'stop_time':'19:00',
        'prohibited_days':[
            'Saturday',
            'Sunday'
        ]
    }

    # Initialize as Schedule from a Dict
    my_schedule = stricture.Schedule.from_dict(schedule_dict)

    # Initialize Stricture with...
    #   schedule
    #   launch_func
    #   pause_func
    #   resume_func
    #   is_alive_func
    #   condition_func + condition_args
    dummy_stricture = stricture.Stricture(
        schedule=my_schedule,
        launch_func=dummy.api_launch,
        pause_func=dummy.api_pause,
        resume_func=dummy.api_resume,
        is_alive_func=dummy.api_is_alive,
        condition_func=my_condition,
        condition_args=['https://example.com/'],
    )

    dummy_stricture.execute() # Runs the process according to the schedule

    print('Done!')

if __name__ == "__main__":
    main()
```

### `schedule: stricture.Schedule`
The `Schedule` that the stricture should apply to the process. When no schedule is provided, always returns `True` when checked and has no affect on execution.

### `sleep_duration: int`
The time between checking if the process is alive and if any given condition is met. Default value is `10` seconds.

### `launch_func: function`
The function to be executed in place of the `launch` function in the `execute` template.

### `launch_args: list[*]`
A `list` of arguments to be passed to the `launch` method (supplied by the `launch_func` attribute) when called.

### `launch_kwargs: dict{str,*}`
A `dict` of keyword arguments to be passed to the `launch` method (supplied by the `launch_func` attribute) when called.

### `pause_func: function`
The function to be executed in place of the `pause` function in the `execute` template.

### `pause_args: list[*]`
A `list` of arguments to be passed to the `pause` method (supplied by the `pause_func` attribute) when called.

### `pause_kwargs: dict{str,*}`
A `dict` of keyword arguments to be passed to the `pause` method (supplied by the `pause_func` attribute) when called.

### `resume_func: function`
The function to be executed in place of the `resume` function in the `execute` template.

### `resume_args: list[*]`
A `list` of arguments to be passed to the `resume` method (supplied by the `resume_func` attribute) when called.

### `resume_kwargs: dict{str,*}`
A `dict` of keyword arguments to be passed to the `resume` method (supplied by the `resume_func` attribute) when called.

### `is_alive_func: function`
The function to be executed in place of the `is_alive` function in the `execute` template.

### `is_alive_args: list[*]`
A `list` of arguments to be passed to the `is_alive` method (supplied by the `is_alive_func` attribute) when called.

### `is_alive_kwargs: dict{str,*}`
A `dict` of keyword arguments to be passed to the `is_alive` method (supplied by the `is_alive_func` attribute) when called.

### `condition_func: function`
The function to be executed in place of the `condition` function in the `execute` template.

### `condition_args: list[*]`
A `list` of arguments to be passed to the `condition` method (supplied by the `condition_func` attribute) when called.

### `condition_kwargs: dict{str,*}`
A `dict` of keyword arguments to be passed to the `condition` method (supplied by the `condition_func` attribute) when called.


### `execute_func: function`
The function to be executed as the `execute` template.

### `execute_args: list[*]`
A `list` of arguments to be passed to the `execute` method (supplied by the `execute_func` attribute) when called.

### `execute_kwargs: dict{str,*}`
A `dict` of keyword arguments to be passed to the `execute` method (supplied by the `execute_func` attribute) when called.


## Methods
  - [`set_schedule`](#set_schedule)
  - [`set_launch`](#set_launch)
  - [`set_pause`](#set_pause)
  - [`set_resume`](#set_resume)
  - [`set_is_alive`](#set_is_alive)
  - [`set_condition`](#set_condition)
  - [`set_execute`](#set_execute)
  - [`execute`](#execute)


### `set_schedule`
Used to set the `Schedule` that the stricture should apply to the process.

##### Example
```python
my_schedule = Schedule(
    start_time='09:30',
    stop_time='17:00',
)

my_process_stricture = Stricture()
my_process_stricture.set_schedule(my_schedule)
```

### `set_launch`
Used to set the `launch` function that the stricture should apply to the process (supplied by `launch_func`). Similar to instantiation usage. Also takes `launch_args` and `launch_kwargs` as keyword arguments.

### `set_pause`
Used to set the `pause` function that the stricture should apply to the process (supplied by `pause_func`). Similar to instantiation usage. Also takes `pause_args` and `pause_kwargs` as keyword arguments.

### `set_resume`
Used to set the `resume` function that the stricture should apply to the process (supplied by `resume_func`). Similar to instantiation usage. Also takes `resume_args` and `resume_kwargs` as keyword arguments.

### `set_is_alive`
Used to set the `is_alive` function that the stricture should apply to the process (supplied by `is_alive_func`). Similar to instantiation usage. Also takes `is_alive_args` and `is_alive_kwargs` as keyword arguments.

### `set_condition`
Used to set the `condition` function that the stricture should apply to the process (supplied by `condition_func`). Similar to instantiation usage. Also takes `condition_args` and `condition_kwargs` as keyword arguments.

### `set_execute`
Used to set the `execute` function that the stricture should apply to the process (supplied by `execute_func`). Similar to instantiation usage. Also takes `execute_args` and `execute_kwargs` as keyword arguments.

### `execute`
Applies the stricture to the process, starting and stopping it as needed based on the conditions and schedule. Call when ready. See any earlier examples.