![](https://raw.githubusercontent.com/moorejacob2017/Stricture/master/logos/stricture_logo_white_long.png)

Stricture is a python package that provides classes and a CLI tool for easy scheduling, automating, and managing of specific operations.

Currently, Stricture provides 5 classes:
- `Schedule` - Used to determine if the current date and time falls within a user defined schedule. Provides a variety of functionality that promotes human readable schedules, ranging from broad week-to-week bases, to granular date and time ranges.
- `Stricture` - A class used to abstract the idea of starting and stopping a specified operation or process based on a `Schedule` or other condition. User supplied functions are orchestrated by a templated function to launch, pause, resume, and check conditions for an operation.
- `ProcessStricture` - A differentiated `Stricture` used to start and stop local system processes given a `Schedule` or other condition.
- `Command` - A basic utility for easily running terminal commands and collecting their output.
- `CommandStricture` - A differentiated `Stricture` used to start and stop terminal commands (using the `Command` Class) given a `Schedule` or other condition.

Please review the [Stricture Documentation](https://github.com/moorejacob2017/Stricture/) for more information.


## Stricture CLI Tool

The Stricture Python Package ships with a CLI tool for starting and stopping a process or command given a schedule. This is done by sending a `SIGSTOP` to the process when the date and time are outside the schedule and a `SIGCONT` when the date and time are in the schedule.

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



