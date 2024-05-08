# `CommandStricture` Class

- [About](#about)
- [Logging](#logging)
- [Instantiation](#instantiation)
  - [`command: str`](#command-str)
  - [`schedule: stricture.Schedule`](#schedule-strictureschedule)
  - [`sleep_duration: int`](#sleep_duration-int)
  - [`condition_func: function`](#condition_func-function)
  - [`condition_args: list[*]`](#condition_args-list)
  - [`condition_kwargs: dict{str,*}`](#condition_kwargs-dictstr)
- [Methods](#methods)
  - [`set_schedule`](#set_schedule)
  - [`set_condition`](#set_condition)
  - [`execute`](#execute)

## About
The `CommandStricture` is a child class of the `Stricture` class used to apply scheduling and conditions to a terminal command. Command execution and output is managed by the `Command` class.

__WARNING:__ Similar to the `Stricture` class, monkey patching methods and mondifying attributes directly is not recommended. Use the provided methods to set attributes and functionality to keep from breaking something.

<!--__WARNING:__ Currently unsupported on Windows systems. Windows support is in progress and is currently planned for a future release.-->

##### Example 1
A simple `CommandStricture` that uses a `Schedule` to start and stop a command
```python
from stricture import CommandStricture, Schedule

# Start and Stop command according to schedule.
# Schedule:
#   9:30am-5:00pm everyday

# Set the Schedule
my_schedule = Schedule(
    start_time='09:30',
    stop_time='17:00',
)

# Set the CommandStricture
my_command_stricture = CommandStricture(
    command="./my_script.sh",
    schedule=my_schedule,
)

# Apply the stricture
my_command_stricture.execute()
```

##### Example 2
A `CommandStricture` that uses a `Schedule` and a specific condition to start and stop a command. It only continues when the current date and time is in schedule and if the condition is met.
```python
import requests
from stricture import CommandStricture, Schedule

# Start and Stop command from 9:30am-5:00pm 
# everyday and if https://example.com/ is reachable.
# If not reachable, then pause. Resume when reachable again.
# Check every 60 seconds

# If https://example.com/ is reached with an 
# http 200, return True, else False
def my_condition():
    try:
        response = requests.get('https://example.com/', timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False

# Schedule:
#   9:30am-5:00pm everyday
my_schedule = Schedule(
    start_time='09:30',
    stop_time='17:00',
)

my_command_stricture = CommandStricture(
    command="./my_script.sh"
    schedule=my_schedule,
    sleep_duration=60, # Check if alive every 60 seconds
    condition_func=my_condition
)

# Apply the stricture
my_command_stricture.execute()
```

## Logging
The `CommandStricture` class provides basic logging, but not by default. One can monitor stricture execution by including the following in their script:

```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %Z'
)
```


## Instantiation
- [`command: str`](#command-str)
- [`schedule: stricture.Schedule`](#schedule-strictureschedule)
- [`sleep_duration: int`](#sleep_duration-int)
- [`condition_func: function`](#condition_func-function)
- [`condition_args: list[*]`](#condition_args-list)
- [`condition_kwargs: dict{str,*}`](#condition_kwargs-dictstr)

### `command: str`
The command to apply the stricture to. Is required.

### `schedule: stricture.Schedule`
The `Schedule` to use when applying the stricture.

##### Example
```python
# Start and Stop command from 9:30am-5:00pm everyday 

my_schedule = Schedule(
    start_time='09:30',
    stop_time='17:00',
)


my_command_stricture = CommandStricture(
    command="./my_script.sh",
    schedule=my_schedule
)

my_command_stricture.execute()

```

### `sleep_duration: int`
The time between checking if the command is alive and if any given condition is met. Default value is `10` seconds.

### `condition_func: function`
The function to be executed in place of the `condition` function in the `execute` template.

```python
# Start and Stop command based on a specific condition.
# The condition is if https://example.com/ is reachable.
# If not reachable, then pause. Resume when reachable again.

def my_condition():
    try:
        response = requests.get('https://example.com/', timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False


my_command_stricture = CommandStricture(
    command="./my_script.sh",
    condition_func=my_condition
)

my_command_stricture.execute()
```

### `condition_args: list[*]`
A `list` of arguments to be passed to the `condition` method (supplied by the `condition_func` attribute) when called.

```python
# Start and Stop command based on a specific condition.
# The condition is if a given url is reachable.
# If not reachable, then pause. Resume when reachable again.

def my_condition(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False


my_command_stricture = CommandStricture(
    command="./my_script.sh",
    condition_func=my_condition,
    condition_args=[
        'https://example.com/'
    ]
)

my_command_stricture.execute()
```

### `condition_kwargs: dict{str,*}`
A `dict` of keyword arguments to be passed to the `condition` method (supplied by the `condition_func` attribute) when called.

__NOTE:__ Will be ran consecutively at times, especially at the beginning. Include delays as needed.

```python
# Start and Stop command based on a specific condition.
# The condition is if a given url is reachable.
# If not reachable, then pause. Resume when reachable again.

def my_condition(url=None):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False


my_command_stricture = CommandStricture(
    command="./my_script.sh",
    condition_func=my_condition,
    condition_kwargs={
        'url':'https://example.com/'
    }
)

my_command_stricture.execute()
```

## Methods

- [`set_schedule`](#set_schedule)
- [`set_condition`](#set_condition)
- [`execute`](#execute)

### `set_schedule`
Used to set the `Schedule` that the stricture should apply to the command.

##### Example
```python
my_schedule = Schedule(
    start_time='09:30',
    stop_time='17:00',
)

my_command_stricture = CommandStricture("./my_script.sh")
my_command_stricture.set_schedule(my_schedule)
my_command_stricture.execute()
```

### `set_condition`
Used to set the `condition` function that the stricture should apply to the command (supplied by `condition_func`). Similar to instantiation usage. Also takes `condition_args` and `condition_kwargs` as keyword arguments.

##### Example
```python
# Start and Stop command based on a specific condition.
# The condition is if a given url is reachable.
# If not reachable, then pause. Resume when reachable again.

def my_condition(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False


my_command_stricture = CommandStricture("./my_script.sh")
my_command_stricture.set_condition(
    condition_func=my_condition,
    condition_args=[
        'https://example.com/'
    ]
)
my_command_stricture.execute()
```


### `execute`
Applies the stricture to the command, starting and stopping it as needed based on the conditions and schedule. Returns the executed `Command` object when finished. Call when ready.

##### Example
```python
my_command_stricture = CommandStricture("./my_script.sh")
results = my_command_stricture.execute()

print(type(results))
#<class 'stricture.commandstricture.Command'>
```
