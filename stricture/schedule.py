import json
import yaml
import pytz
import freezegun
from time import sleep
from dateutil import parser
from datetime import datetime, time
from tzlocal import get_localzone # pip install tzlocal

def normalize_days(days):
    # Set of valid day names in lowercase for case-insensitive matching
    valid_days = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}
    
    # List to store normalized day names
    normalized_days = []
    
    # Check each day in the input array
    for day in days:
        # Convert day string to lowercase for case-insensitive matching
        lower_day = day.lower()
        
        # Check if the day is valid
        if lower_day not in valid_days:
            raise ValueError(f"Invalid day of the week: {day}")
        
        # Normalize the day name (capitalize first letter)
        normalized_day = lower_day.capitalize()  # Capitalize first letter
        normalized_days.append(normalized_day)
    
    # Return the list of normalized day names
    return normalized_days


def string_to_date(date_string):
    try:
        date_string = date_string.strip()
        # Split the date string into parts
        parts = date_string.split(' ')
        
        # Check if a timezone is provided
        if len(parts) == 3:
            datetime_part = ' '.join(parts[:2])
            timezone_name = parts[-1]
        else:
            datetime_part = date_string
            timezone_name = str(get_localzone())  # Default to UTC if no timezone provided
        
        # Parse the datetime part
        naive_date = datetime.strptime(datetime_part, "%Y-%m-%d %H:%M")
        
        # Convert to the specified timezone or UTC
        timezone = pytz.timezone(timezone_name)
        localized_date = timezone.localize(naive_date)
        
        return localized_date
    
    except ValueError as e:
        #print(e)
        raise ValueError("Error: Invalid date string format (%Y-%m-%d %H:%M [%Z])") from e


class Schedule:
    """
    ExecutionScheduler class to determine whether a command should be executed at a specific time.

    Attributes:
    - start_time: (datetime.time) The time of day at which the allowed execution period starts.
    - stop_time: (datetime.time) The time of day at which the allowed execution period ends.
    - unrestricted_days: (list) The days of the week on which execution is allowed at any time.
    - restricted_days: (list) The days of the week on which execution is allowed, but restricted.
    - prohibited_days: (list) The days of the week on which execution is prohibited.
    - specific_dates: (list) A list of dictionaries that define special periods of time with either unlimited execution or no execution.
    - timezone: (str) The timezone to use when checking the current time.
    - assume: (str) Default restricted
    """

    def __init__(
            self,
            timezone=None,
            start_time=None,
            stop_time=None,
            unrestricted_days=[],
            restricted_days=[],  
            prohibited_days=[],
            specific_dates=[],
            assume=None,
        ):
        if timezone == None:
            timezone = str(get_localzone())

        if start_time == None:
            start_time = "00:00"
        
        if stop_time == None:
            stop_time = "00:00"

        restricted_days = normalize_days(restricted_days)
        unrestricted_days = normalize_days(unrestricted_days)
        prohibited_days = normalize_days(prohibited_days)



        all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        unlisted_days = [day for day in all_days if day not in unrestricted_days and day not in prohibited_days and day not in restricted_days]
        
        if assume == None:
            assume = 'restricted'
        elif not isinstance(assume, str):
            raise ValueError(f"Schedule.assume expected str, but {type(assume).__name__}")
        
        # If restricted is the only one with values, assume prohibited for unlisted
        #if not assume and not restricted == [] and unrestricted == [] and prohibited == []:
        #    pass
        # If no values, assume restricted for unlisted
        #if not assume and not restricted == [] and unrestricted == [] and prohibited == []:
        #    pass
        # If prohibited is the only one with values, assume unrestricted for unlisted
        #if not assume and not prohibited == [] and unrestricted == [] and restricted == []:
        #    pass
        # If unrestricted is the only one with values, assume prohibited for unlisted
        #if not assume and not unrestricted == [] and prohibited == [] and restricted == []:
        #    pass

        if assume.lower() == 'restricted':
            restricted_days += unlisted_days
        elif assume.lower() == 'unrestricted':
            unrestricted_days += unlisted_days
        elif assume.lower() == 'prohibited':
            prohibited_days += unlisted_days
        else:
            raise ValueError(f"Schedule.assume expected value of \"restricted\", \"unrestricted\", or \"prohibited\", but got \"{assume}\"")

        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, '%H:%M').time()
        elif not isinstance(start_time, time):
            raise ValueError(f"Schedule.start_time expected a str or a datetime.time, but got {type(start_time).__name__}")
        if isinstance(stop_time, str):
            stop_time = datetime.strptime(stop_time, '%H:%M').time()
        elif not isinstance(stop_time, time):
            raise ValueError(f"Schedule.start_time expected a str or a datetime.time, but got {type(stop_time).__name__}")


        for specific_date in specific_dates:
            if 'start_time' in specific_date and 'stop_time' in specific_date:
                sd_start_time = specific_date['start_time']
                if isinstance(sd_start_time, str):
                    specific_date['start_time'] = datetime.strptime(sd_start_time, '%H:%M').time()
                elif not isinstance(sd_start_time, time):
                    raise ValueError(f"Schedule.start_time expected a str or a datetime.time, but got {type(sd_start_time).__name__}")
                sd_stop_time = specific_date['stop_time']
                if isinstance(sd_stop_time, str):
                    specific_date['stop_time'] = datetime.strptime(sd_stop_time, '%H:%M').time()
                elif not isinstance(sd_stop_time, time):
                    raise ValueError(f"Schedule.stop_time expected a str or a datetime.time, but got {type(sd_stop_time).__name__}")

        self.assume = assume
        self.timezone = pytz.timezone(timezone)
        self.start_time = start_time
        self.stop_time = stop_time
        self.restricted_days = restricted_days
        self.unrestricted_days = unrestricted_days
        self.prohibited_days = prohibited_days
        self.specific_dates = specific_dates

    def __str__(self):
        d = {
            "timezone": str(self.timezone),
            "start_time": str(self.start_time)[:-3],
            "stop_time": str(self.stop_time)[:-3],
            "unrestricted_days": ', '.join(self.unrestricted_days),
            "restricted_days": ', '.join(self.restricted_days),
            "prohibited_days": ', '.join(self.prohibited_days),
            "specific_dates": self.specific_dates,
            "assume": self.assume,
        }
        for specific_date in d["specific_dates"]:
            if 'start_time' in specific_date and 'stop_time' in specific_date:
                sd_start_time = specific_date['start_time']
                specific_date['start_time'] = str(sd_start_time)[:-3]
                sd_stop_time = specific_date['stop_time']
                specific_date['stop_time'] = str(sd_stop_time)[:-3]

        return json.dumps(d, indent=4)
        

    def _time_in_range(self, start, end, x):
        """
        Check whether a given time is within a range.

        Args:
        - start: (datetime.time) The start of the time range.
        - end: (datetime.time) The end of the time range.
        - x: (datetime.time) The time to check.

        Returns:
        - (bool) True if the time is within the range, False otherwise.
        """
        if start == end:
            return True
        elif start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end

    def _get_day_of_week(self, date):
        """
        Get the day of the week for a given date.

        Args:
        - date: (datetime.date) The date to check.

        Returns:
        - (str) The day of the week.
        """
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return days[date.weekday()]
    
    
    def test_schedule(self, date):
        test_date = string_to_date(date)
        with freezegun.freeze_time(test_date):
            r = self.check_schedule()
        return r

    def check_schedule(self):
        """
        Determine whether a command can be executed at the current time.
        If the current day has not provided to the schedule, assumes false.

        Returns:
        - (bool) True if the command can be executed, False otherwise.
        """
        now = datetime.now(self.timezone)
        now_time = now.time()
        now_date = now.date()
        now_day = self._get_day_of_week(now)

        for specific_date in self.specific_dates:
            if 'start_date' in specific_date and 'stop_date' in specific_date:
                start_date = parser.parse(specific_date['start_date']).date()
                stop_date = parser.parse(specific_date['stop_date']).date()
                if start_date <= now_date <= stop_date:
                    if specific_date['mode'] == 'unrestricted':
                        return True
                    elif specific_date['mode'] == 'prohibited':
                        return False
                    elif specific_date['mode'] == 'restricted':
                        return self._time_in_range(
                            specific_date['start_time'],
                            specific_date['stop_time'],
                            #datetime.strptime(specific_date['start_time'], '%H:%M').time(),
                            #datetime.strptime(specific_date['stop_time'], '%H:%M').time(),
                            now_time
                        )

        if now_day in self.unrestricted_days:
            return True

        if now_day in self.prohibited_days:
            return False

        if now_day in self.restricted_days:
            return self._time_in_range(self.start_time, self.stop_time, now_time)

        return False
        
    def to_dict(self):
        d = {
            "assume": self.assume,
            "timezone": self.timezone,
            "start_time": self.start_time,
            "stop_time": self.stop_time,
            "unrestricted_days": self.unrestricted_days,
            "restricted_days": self.restricted_days,
            "prohibited_days": self.prohibited_days,
            "specific_dates": self.specific_dates,
        }
        return d
    
    def to_str(self):
        return self.__str__()
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            assume=data.get('assume', 'restricted'),
            timezone=data.get('timezone', None),
            start_time=data.get('start_time', None),
            stop_time=data.get('stop_time', None),
            unrestricted_days=data.get('unrestricted_days', []),
            restricted_days=data.get('restricted_days', []),
            prohibited_days=data.get('prohibited_days', []),
            specific_dates=data.get('specific_dates', []),
        )

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(
            assume=data.get('assume', 'restricted'),
            timezone=data.get('timezone', None),
            start_time=data.get('start_time', None),
            stop_time=data.get('stop_time', None),
            unrestricted_days=data.get('unrestricted_days', []),
            restricted_days=data.get('restricted_days', []),
            prohibited_days=data.get('prohibited_days', []),
            specific_dates=data.get('specific_dates', []),
        )
    
    @classmethod
    def from_yaml(cls, yaml_string):
        config = yaml.safe_load(yaml_string)
        if not isinstance(config, dict):
            raise ValueError('Invalid YAML formatting.')
        return cls(
            assume=config.get('assume', 'restricted'),
            timezone=config.get('timezone', None),
            start_time=config.get('start_time', None),
            stop_time=config.get('stop_time', None),
            unrestricted_days=config.get('unrestricted_days', []),
            restricted_days=config.get('restricted_days', []),
            prohibited_days=config.get('prohibited_days', []),
            specific_dates=config.get('specific_dates', [])
        )
    
    @classmethod
    def from_json_file(cls, json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
        return cls(
            assume=data.get('assume', 'restricted'),
            timezone=data.get('timezone', None),
            start_time=data.get('start_time', None),
            stop_time=data.get('stop_time', None),
            unrestricted_days=data.get('unrestricted_days', []),
            restricted_days=data.get('restricted_days', []),
            prohibited_days=data.get('prohibited_days', []),
            specific_dates=data.get('specific_dates', []),
        )
    
    @classmethod
    def from_yaml_file(cls, yaml_file):
        with open(yaml_file, 'r') as file:
            config = yaml.safe_load(file)
        if not isinstance(config, dict):
            raise ValueError('Invalid YAML formatting.')
        return cls(
            assume=config.get('assume', 'restricted'),
            timezone=config.get('timezone', None),
            start_time=config.get('start_time', None),
            stop_time=config.get('stop_time', None),
            unrestricted_days=config.get('unrestricted_days', []),
            restricted_days=config.get('restricted_days', []),
            prohibited_days=config.get('prohibited_days', []),
            specific_dates = config.get('specific_dates', [])
        )

