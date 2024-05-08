# Stricture CLI Tool

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

WARNING: Commands passed in with --command run at the speed of python, which is SLOW.
         Running a command normally, then applying a stricture using the PID with --pid keeps
         the command from running slowly.
    
Examples:
    stricture -s my_schedule.yml -c "ping -c 1000 192.168.1.1"
    stricture -s my_schedule.yml -qoe -c "./my_script.sh"
    stricture -s my_schedule.json -p 13019

Example schedule format (see "Schedule" docs):
=======[YAML]========
assume: "restricted"
timezone: "US/Central"
start_time: "09:30"
stop_time: "17:00"
restricted_days:
  - "Monday"
  - "Tuesday"
  - "Wednesday"
  - "Thursday"
  - "Friday"
unrestricted_days:
  - "Saturday"  
prohibited_days:
  - "Sunday"
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
=====================
```

