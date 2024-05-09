

![link](logos/stricture_logo_white_long.png)


Stricture is a python package that provides classes and a CLI tool for easy scheduling, automating, and managing of specific operations.

Currently, Stricture provides 5 classes:
- `Schedule` - Used to determine if the current date and time falls within a user defined schedule. Provides a variety of functionality that promotes human readable schedules, ranging from broad week-to-week bases, to granular date and time ranges.
- `Stricture` - A class used to abstract the idea of starting and stopping a specified operation or process based on a `Schedule` or other condition. User supplied functions are orchestrated by a templated function to launch, pause, resume, and check conditions for an operation.
- `ProcessStricture` - A differentiated `Stricture` used to start and stop local system processes given a `Schedule` or other condition.
- `Command` - A basic utility for easily running terminal commands and collecting their output.
- `CommandStricture` - A differentiated `Stricture` used to start and stop terminal commands (using the `Command` Class) given a `Schedule` or other condition.

## Install
```bash
pip install Stricture
```

## Stricture CLI Tool

The Stricture Python Package ships with a CLI tool for quickly applying a `Schedule` and `Stricture` to a command or running process.

```
usage: stricture [-h] -s SCHEDULE [-q] [-o] [-e] (-p PID | -c COMMAND)

Apply a stricture to a command or process to execute based on a given schedule.

options:
  -h, --help            show this help message and exit
  -s SCHEDULE, --schedule SCHEDULE
                        Schedule file in JSON or YAML format.
  -q, --quiet           Quiet mode. No stricture logging output.
  -o, --stdout          Print STDOUT of command (--command only).
  -e, --stderr          Print STDERR of command (--command only).
  -p PID, --pid PID     Process ID. Required if no command is provided.
  -c COMMAND, --command COMMAND
                        Command to execute. Required if no PID is provided.

Examples:
    stricture -s my_schedule.yml -c "ping -c 1000 192.168.1.1"
    stricture -s my_schedule.yml -qoe -c "./my_script.sh"
    stricture -s my_schedule.json -p 13019
```


## Making a schedule in YAML
`Schedules` have many different ways to be instantiated and initialized. On of the easiest ways to create a schedule is to import it from a yaml file with `from_yaml_file`. Below is an explaination of how to format a schedule with yaml.
```yaml
# Days are classified into 1 of 3 modes: restricted, unrestricted, and prohibited.
#   restricted - Days are considered in schedule, but only for the
#                time range defined by start_time and stop_time.
#   unrestricted - All 24 hours of the day are considered in the schedule.
#   prohibited - All 24 hours of the day are coonsidered out of schedule.

# assume:
#   The mode to use for days of the week that are not listed in the schedule.
#   Can either be unrestricted, restricted, or prohibited.
#   Defaults to restricted when not set.
assume: "restricted"

# timezone:
#   The timezone to use when checking the schedule.
#   Uses pytz timezones (Olson Timezone IDs).
#   Defaults to the system timezone when not set.
timezone: "US/Central"

# start_time:
#   Defines what time the schedule range starts for every restricted day.
#   Uses 24-Hour Format.
#   Defaults to 00:00 when not set.
start_time: "09:30"

# stop_time:
#   Defines what time the schedule range stops for every restricted day.
#   Uses 24-Hour Format.
#   Defaults to 00:00 when not set.
stop_time: "17:00"

# restricted_days:
#   A list of days of the week that should
#   have the start_time and stop_time applied to.
restricted_days:
  - "Monday"
  - "Tuesday"
  - "Wednesday"
  - "Thursday"
  - "Friday"

# unrestricted_days:
#   A list of days of the week that should 
#   have all 24 hours considered as in the schedule.
unrestricted_days:
  - "Saturday"

# prohibited_days:
#   A list of days of the week that should 
#   have all 24 hours considered as out of the schedule.
prohibited_days:
  - "Sunday"

# specific_dates:
#   A list of specific date ranges that overides the main
#   start_time, stop_time, and mode.
#   Useful for special occasions or for more granular
#   control.
#       mode - The mode to use for the range.
#       start_date - The start of the date range (YYYY-MM-DD format).
#       stop_date - The end of the date range (inclusively) (YYYY-MM-DD format).
#       start_time - The start_time to use when the mode for the range is restricted.
#       stop_time - The stop_time to use when the mode for the range is restricted.
specific_dates:
  - mode: "unrestricted"
    start_date: "2024-12-12"
    stop_date: "2024-12-23"
  - mode: "prohibited"
    start_date: "2024-12-24"
    stop_date: "2024-12-26"
  - mode: "restricted"
    start_date: "2024-12-27"
    stop_date: "2024-12-31"
    start_time: "18:00"
    stop_time: "08:30"
```


## Documentation
- [Stricture Demo](./example/Example.md)
  - [Why?](./example/Example.md#why)
  - [A DummyAPI Example](./example/Example.md#a-dummyapi-example)
  - [Applying a `Stricture` to the API](./example/Example.md#applying-a-stricture-to-the-api)
- [Stricture CLI Tool](./docs/Stricture_CLI.md)
- [`Schedule` Class](./docs/Schedule.md)
  - [About](./docs/Schedule.md#about)
  - [Attributes](./docs/Schedule.md#attributes)
    - [`timezone: str`](./docs/Schedule.md#timezone-str)
    - [`start_time: datetime.time`](./docs/Schedule.md#start_time-datetimetime)
    - [`stop_time: datetime.time`](./docs/Schedule.md#stop_time-datetimetime)
    - [`unrestricted_days: list[str]`](./docs/Schedule.md#unrestricted_days-liststr)
    - [`restricted_days: list[str]`](./docs/Schedule.md#restricted_days-liststr)
    - [`prohibited_days: list[str]`](./docs/Schedule.md#prohibited_days-liststr)
    - [`specific_dates: list[dict]`](./docs/Schedule.md#specific_dates-listdict)
    - [`assume: str`](./docs/Schedule.md#assume-str)
  - [Methods](./docs/Schedule.md#methods)
    - [`check_schedule`](./docs/Schedule.md#check_schedule)
    - [`test_schedule`](./docs/Schedule.md#test_schedule)
    - [`from_dict`](./docs/Schedule.md#from_dict)
    - [`from_json`](./docs/Schedule.md#from_json)
    - [`from_yaml`](./docs/Schedule.md#from_yaml)
    - [`from_json_file`](./docs/Schedule.md#from_json_file)
    - [`from_yaml_file`](./docs/Schedule.md#from_yaml_file)
    - [`to_str`](./docs/Schedule.md#to_str)
    - [`to_dict`](./docs/Schedule.md#to_dict)
  - [Timezones](./docs/Schedule.md#timezones)
- [`Stricture` Class](./docs/Stricture.md)
  - [About](./docs/Stricture.md#about)
  - [Logging](./docs/Stricture.md#logging)
  - [Abstract Method Behaviors & Requirements](./docs/Stricture.md#abstract-method-behaviors--requirements)
    - [`launch` (Optional)](./docs/Stricture.md#launch-optional)
    - [`pause` (Required)](./docs/Stricture.md#pause-required)
    - [`resume` (Required)](./docs/Stricture.md#resume-required)
    - [`is_alive` (Required)](./docs/Stricture.md#is_alive-required)
    - [`condition` (Optional)](./docs/Stricture.md#condition-optional)
    - [`execute` (Optional)](./docs/Stricture.md#execute-optional)
  - [Instantiation](./docs/Stricture.md#instantiation)
    - [Instantiation Example](./docs/Stricture.md#instantiation-example)
    - [`schedule: stricture.Schedule`](./docs/Stricture.md#schedule-strictureschedule)
    - [`sleep_duration: int`](./docs/Stricture.md#sleep_duration-int)
    - [`launch_func: function`](./docs/Stricture.md#launch_func-function)
    - [`launch_args: list[*]`](./docs/Stricture.md#launch_args-list)
    - [`launch_kwargs: dict{str,*}`](./docs/Stricture.md#launch_kwargs-dictstr)
    - [`pause_func: function`](./docs/Stricture.md#pause_func-function)
    - [`pause_args: list[*]`](./docs/Stricture.md#pause_args-list)
    - [`pause_kwargs: dict{str,*}`](./docs/Stricture.md#pause_kwargs-dictstr)
    - [`resume_func: function`](./docs/Stricture.md#resume_func-function)
    - [`resume_args: list[*]`](./docs/Stricture.md#resume_args-list)
    - [`resume_kwargs: dict{str,*}`](./docs/Stricture.md#resume_kwargs-dictstr)
    - [`is_alive_func: function`](./docs/Stricture.md#is_alive_func-function)
    - [`is_alive_args: list[*]`](./docs/Stricture.md#is_alive_args-list)
    - [`is_alive_kwargs: dict{str,*}`](./docs/Stricture.md#is_alive_kwargs-dictstr)
    - [`condition_func: function`](./docs/Stricture.md#condition_func-function)
    - [`condition_args: list[*]`](./docs/Stricture.md#condition_args-list)
    - [`condition_kwargs: dict{str,*}`](./docs/Stricture.md#condition_kwargs-dictstr)
    - [`execute_func: function`](./docs/Stricture.md#execute_func-function)
    - [`execute_args: list[*]`](./docs/Stricture.md#execute_args-list)
    - [`execute_kwargs: dict{str,*}`](./docs/Stricture.md#execute_kwargs-dictstr)
  - [Methods](./docs/Stricture.md#methods)
    - [`set_schedule`](./docs/Stricture.md#set_schedule)
    - [`set_launch`](./docs/Stricture.md#set_launch)
    - [`set_pause`](./docs/Stricture.md#set_pause)
    - [`set_resume`](./docs/Stricture.md#set_resume)
    - [`set_is_alive`](./docs/Stricture.md#set_is_alive)
    - [`set_condition`](./docs/Stricture.md#set_condition)
    - [`set_execute`](./docs/Stricture.md#set_execute)
    - [`execute`](./docs/Stricture.md#execute)
- [`ProcessStricture` Class](./docs/ProcessStricture.md)
  - [About](./docs/ProcessStricture.md#about)
  - [Logging](./docs/ProcessStricture.md#logging)
  - [Instantiation](./docs/ProcessStricture.md#instantiation)
    - [`pid: int`](./docs/ProcessStricture.md#pid-int)
    - [`schedule: stricture.Schedule`](./docs/ProcessStricture.md#schedule-strictureschedule)
    - [`sleep_duration: int`](./docs/ProcessStricture.md#sleep_duration-int)
    - [`condition_func: function`](./docs/ProcessStricture.md#condition_func-function)
    - [`condition_args: list[*]`](./docs/ProcessStricture.md#condition_args-list)
    - [`condition_kwargs: dict{str,*}`](./docs/ProcessStricture.md#condition_kwargs-dictstr)
  - [Methods](./docs/ProcessStricture.md#methods)
    - [`set_schedule`](./docs/ProcessStricture.md#set_schedule)
    - [`set_condition`](./docs/ProcessStricture.md#set_condition)
    - [`execute`](./docs/ProcessStricture.md#execute)
- [`Command` Class](./docs/Command.md)
  - [About](./docs/Command.md#about)
  - [Instantiation](./docs/Command.md#instantiation)
  - [Attributes](./docs/Command.md#attributes)
    - [`command: str`](./docs/Command.md#command-str)
    - [`started_at: int`](./docs/Command.md#started_at-int)
    - [`finished_at: int`](./docs/Command.md#finished_at-int)
    - [`stdout: str`](./docs/Command.md#stdout-str)
    - [`stderr: str`](./docs/Command.md#stderr-str)
    - [`executed: bool`](./docs/Command.md#executed-bool)
  - [Methods](./docs/Command.md#methods)
    - [`run`](./docs/Command.md#run)
    - [`to_dict`](./docs/Command.md#to_dict)
    - [`to_str`](./docs/Command.md#to_str)
- [`CommandStricture` Class](./docs/CommandStricture.md)
  - [About](./docs/CommandStricture.md#about)
  - [Logging](./docs/CommandStricture.md#logging)
  - [Instantiation](./docs/CommandStricture.md#instantiation)
    - [`command: str`](./docs/CommandStricture.md#command-str)
    - [`schedule: stricture.Schedule`](./docs/CommandStricture.md#schedule-strictureschedule)
    - [`sleep_duration: int`](./docs/CommandStricture.md#sleep_duration-int)
    - [`condition_func: function`](./docs/CommandStricture.md#condition_func-function)
    - [`condition_args: list[*]`](./docs/CommandStricture.md#condition_args-list)
    - [`condition_kwargs: dict{str,*}`](./docs/CommandStricture.md#condition_kwargs-dictstr)
  - [Methods](./docs/CommandStricture.md#methods)
    - [`set_schedule`](./docs/CommandStricture.md#set_schedule)
    - [`set_condition`](./docs/CommandStricture.md#set_condition)
    - [`execute`](./docs/CommandStricture.md#execute)
