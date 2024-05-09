import argparse
import json
import yaml
import os
import logging

import stricture

def check_extension(filename):
    # Extract the file extension
    _, file_extension = os.path.splitext(filename)
    
    # Check the file extension
    if file_extension.lower() == '.yaml' or file_extension.lower() == '.yml':
        return "YAML"
    elif file_extension.lower() == '.json':
        return "JSON"
    else:
        raise ValueError("Unsupported file type. Only YAML (.yaml/.yml) and JSON (.json) extensions are allowed.")

def test_load_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            yaml_data = yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except yaml.YAMLError as exc:
        raise ValueError(f"Error loading YAML from file '{file_path}': {exc}")

def test_load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except json.JSONDecodeError as exc:
        raise ValueError(f"Error loading JSON from file '{file_path}': {exc}")

def main():
    description = "Apply a stricture to a command or process to execute based on a given schedule."
    example_text = '''
    
Examples:
    %(prog)s -s my_schedule.yml -c "ping -c 1000 192.168.1.1"
    %(prog)s -s my_schedule.yml -qoe -c "./my_script.sh"
    %(prog)s -s my_schedule.json -p 13019

Making a schedule in YAML format:
=======[YAML]========
# Days are classified into 1 of 3 modes: restricted, unrestricted, and prohibited
#   restricted - Days are considered in schedule, but only for the
#                time range defined by start_time and stop_time
#   unrestricted - All 24 hours of the day are considered in the schedule
#   prohibited - All 24 hours of the day are coonsidered out of schedule

# assume:
#   The mode to use for days of the week that are not listed in the schedule
#   Can either be unrestricted, restricted, or prohibited
#   Defaults to restricted when not set
assume: "restricted"

# timezone:
#   The timezone to use when checking the schedule
#   Uses pytz timezones (Olson Timezone IDs)
#   Defaults to the system time when not set
timezone: "US/Central"

# start_time:
#   Defines what time the schedule range starts every day
#   24-Hour Format
#   Defaults to 00:00 when not set
start_time: "09:30"

# stop_time:
#   Defines what time the schedule range stops every day
#   24-Hour Format
#   Defaults to 00:00 when not set
stop_time: "17:00"

# restricted_days:
#   A list of days of the week that should 
#   have the start_time and stop_time applied to
restricted_days:
  - "Monday"
  - "Tuesday"
  - "Wednesday"
  - "Thursday"
  - "Friday"

# unrestricted_days:
#   A list of days of the week that should 
#   have all 24 hours considered as in the schedule
unrestricted_days:
  - "Saturday"

# prohibited_days:
#   A list of days of the week that should 
#   have all 24 hours considered as out of the schedule
prohibited_days:
  - "Sunday"

# specific_dates:
#   A list of specific date ranges that overides the main
#   start_time, stop_time, and mode
#   Useful for special occasions or for more granular
#   control
#       mode - The mode to use for the range
#       start_date - The start of the date range
#       stop_date - The end of the date range (inclusively)
#       start_time - The start_time to use when the mode for the range is restricted
#       stop_time - The stop_time to use when the mode for the range is restricted
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
=======[YAML]========
'''

    parser = argparse.ArgumentParser(
        description=description,
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-s', '--schedule', required=True, help="Schedule file in JSON or YAML format.")
    parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode. No stricture logging output.')
    parser.add_argument('-o', '--stdout', action='store_true', help='Print STDOUT of command (--command only).')
    parser.add_argument('-e', '--stderr', action='store_true', help='Print STDERR of command (--command only).')
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--pid', type=int, help="Process ID. Required if no command is provided.")
    group.add_argument('-c', '--command', help="Command to execute. Required if no PID is provided.")
    
    # Parse command-line arguments
    args = parser.parse_args()

    if not args.quiet:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S %Z'  # Include UTC offset in the timestamp
        )

    # Validate stdout and stderr flags based on --command usage
    if args.command is None and (args.stdout or args.stderr):
        parser.error("--stdout or --stderr flags are only valid when using --command.")

    try:
        stype = check_extension(args.schedule)
        if stype == "YAML":
            test_load_yaml(args.schedule)
        elif stype == "JSON":    
            test_load_json(args.schedule)
    except Exception as e:
        print("Error loading schedule file:", e)
        
    if stype == "YAML":
        schedule = stricture.Schedule.from_yaml_file(args.schedule)
    elif stype == "JSON":    
        schedule = stricture.Schedule.from_json_file(args.schedule)
    else:
        print('Congrats! IDK how, but you broke it. Exiting...')
        exit(1)

    if args.pid:
        #print("Process ID provided:", args.pid)
        strict = stricture.ProcessStricture(args.pid)
    elif args.command:
        #print("Command to execute:", args.command)
        strict = stricture.CommandStricture(args.command)
    else:
        print("Either a PID or a command must be provided.")
        exit(1)


    strict.set_schedule(schedule)
    results = strict.execute()

    if args.stdout:
        print("======[STDOUT]======")
        print(results.stdout)
    if args.stderr:
        print("======[STDERR]======")
        print(results.stderr)
    if args.stdout or args.stderr:
        print("====================")
