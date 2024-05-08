# `Command` Class
- [About](#about)
- [Instantiation](#instantiation)
- [Attributes](#attributes)
  - [`command: str`](#command-str)
  - [`started_at: int`](#started_at-int)
  - [`finished_at: int`](#finished_at-int)
  - [`stdout: str`](#stdout-str)
  - [`stderr: str`](#stderr-str)
  - [`executed: bool`](#executed-bool)
- [Methods](#methods)
  - [`run`](#run)
  - [`to_dict`](#to_dict)
  - [`to_str`](#to_str)

## About
The `Command` class is used to easily run terminal commands and store associated information. It acts as a Quality-of-Life wrapper and manager for the `subprocess` module functionality. However, it also addresses certain issues found when using the `subprocess` module.

For example, when running a command with `subprocess.Popen`, deadlocks can occur if the command has a large output. This has been resolved in the `Command` class by using non-blocking file descriptors to continuously read STDOUT and STDERR into seperate streams.

__NOTE:__ Whenever running a terminal command with the `Command` class, there is a heavy speed penalty. This penalty is negligible for basic commands, but can prove bothersome for already long-running commands.

##### Example
```python
from stricture import Command

my_command = Command('echo "Hello, World!"')
my_command.run()

print(my_command)
if my_command.stdout:
    print("======[STDOUT]======")
    print(my_command.stdout)
if my_command.stderr:
    print("======[STDERR]======")
    print(my_command.stderr)
if my_command.stdout or my_command.stderr:
    print("====================")

# OUTPUT:
# {
#     "command": "echo \"Hello, World!\"",
#     "started_at": "2024-05-07 16:24:22",
#     "finished_at": "2024-05-07 16:24:22",
#     "stdout": "Hello, World!\n",
#     "stderr": ""
# }
# ======[STDOUT]======
# Hello, World!
#
# ====================
```

## Instantiation
Requires `command: str`

##### Example
```python
from stricture import Command

my_command = Command('echo "Hello, World!"')
my_command.run()
```

## Attributes

### `command: str`
The command that will be executed.

### `started_at: int`
The Epoch time when the command started execution. Before execution, the value will default to `0`. Gets converted to a string in the format of "%Y-%m-%d %H:%M:%S" when using `__str__` or `to_str`


### `finished_at: int`
The Epoch time when the command finished execution. Before execution, the value will default to `0`.

### `stdout: str`
The STDOUT of the command after execution stored as a `str`.

### `stderr: str`
The STDERR of the command after execution stored as a `str`.


### `executed: bool`
A bool used to check whether a command has been executed. `True` when the command has been executed and `False` when the command has not been executed.


## Methods
### `run`
Runs the `Command`. Reads in the STDOUT and STDERR and stores them in `stdout` and `stderr`. Logs when the the command was started and finished in `started_at` and `finished_at`. Sets `executed` to `True`.

### `to_dict`
Returns the `Command` in `dict` format.

### `to_str`
Returns the `Command` in `str` format. Is a synonym for `__str__`. Can be printed directly without needing to call `to_str`.

##### Example
```python
command_str = my_command.to_str()
command_str = my_command.__str__()
print(my_command) 
```