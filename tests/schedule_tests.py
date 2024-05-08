import unittest
from unittest.mock import patch
#from freezegun import freeze_time

import freezegun
from datetime import datetime, time, timedelta
import pytz

from stricture import Schedule  # Assuming your class is defined in my_class.py


def string_to_date(date_string):
    try:
        parts = date_string.split()
        datetime_part = ' '.join(parts[:2])
        timezone_name = parts[-1]
        naive_date = datetime.strptime(datetime_part, "%Y-%m-%d %H:%M:%S")
        timezone = pytz.timezone(timezone_name)
        localized_date = timezone.localize(naive_date)
        #print("Test Date:", localized_date)
        return localized_date
    except ValueError:
        print("Error: Invalid date string format")
        return None



class TestSchedule(unittest.TestCase):
    def test_within1(self):
        test_date = "2024-05-03 12:00:00 US/Central"
        schedule = Schedule(
            timezone="US/Central",
            start_time='09:00',
            stop_time='17:00'
        )
        with freezegun.freeze_time(string_to_date(test_date)):
            result = schedule.check_schedule()
        self.assertTrue(result)

    def test_within2(self):
        test_date = "2024-05-03 12:00:00 US/Central"
        schedule = Schedule(
            timezone="US/Central",
            start_time='09:00',
            stop_time='17:00',
            restricted_days=['Friday']
        )
        with freezegun.freeze_time(string_to_date(test_date)):
            result = schedule.check_schedule()
        self.assertTrue(result)

    def test_within3(self):
        test_date = "2024-05-03 12:00:00 US/Central"
        schedule = Schedule(
            assume='prohibited',
            timezone="US/Central",
            unrestricted_days=['Friday']
        )
        with freezegun.freeze_time(string_to_date(test_date)):
            result = schedule.check_schedule()
        self.assertTrue(result)

    def test_within4(self):
        test_date = "2024-05-03 12:00:00 US/Central"
        schedule = Schedule(
            assume='unrestricted',
            timezone="US/Central",
            restricted_days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Saturday', 'Sunday'],
        )
        with freezegun.freeze_time(string_to_date(test_date)):
            result = schedule.check_schedule()
        self.assertTrue(result)

    def test_within5(self):
        test_date = "2024-05-03 12:00:00 US/Central"
        schedule = Schedule(
            timezone="US/Central",
            restricted_days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            specific_dates=[
                {
                    'start_date': '2024-05-03',
                    'stop_date': '2024-05-03',
                    'start_time':'09:00',
                    'stop_time':'17:00',
                    'mode': 'restricted'
                },
            ]
        )
        with freezegun.freeze_time(string_to_date(test_date)):
            result = schedule.check_schedule()
        self.assertTrue(result)

    def test_within6(self):
        test_date = "2024-05-03 12:00:00 US/Central"
        schedule = Schedule(
            timezone="US/Central",
            restricted_days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            specific_dates=[
                {
                    'start_date': '2024-05-03',
                    'stop_date': '2024-05-03',
                    'mode': 'unrestricted'
                },
            ]
        )
        with freezegun.freeze_time(string_to_date(test_date)):
            result = schedule.check_schedule()
        self.assertTrue(result)

    def test_within7(self):
        test_date = "2024-05-03 00:00:00 US/Central"
        schedule = Schedule(
            timezone="US/Central",
            start_time='00:00',
            stop_time='00:00'
        )
        with freezegun.freeze_time(string_to_date(test_date)):
            result = schedule.check_schedule()
        self.assertTrue(result)

    def test_within8(self):
        test_date = "2024-05-03 00:00:00 US/Central"
        schedule = Schedule(
            timezone="US/Central",
            start_time='17:00',
            stop_time='09:00'
        )
        with freezegun.freeze_time(string_to_date(test_date)):
            result = schedule.check_schedule()
        self.assertTrue(result)

    def test_within9(self):
        test_date = "2024-05-02 20:00:00 US/Central"
        schedule = Schedule(
            timezone="US/Central",
            start_time='17:00',
            stop_time='09:00'
        )
        with freezegun.freeze_time(string_to_date(test_date)):
            result = schedule.check_schedule()
        self.assertTrue(result)

    def test_within10(self):
        test_date = "2024-05-02 20:00:00 US/Central"
        schedule = Schedule(
            timezone="US/Central",
        )
        with freezegun.freeze_time(string_to_date(test_date)):
            result = schedule.check_schedule()
        self.assertTrue(result)

    #==================================================================================================

    def test_outside1(self):
        test_date = "2024-05-03 18:00:00 US/Central"
        schedule = Schedule(
            timezone="US/Central",
            start_time='09:00',
            stop_time='17:00'
        )
        with freezegun.freeze_time(string_to_date(test_date)):
            result = schedule.check_schedule()
        self.assertFalse(result)

    def test_outside2(self):
        test_date = "2024-05-03 12:00:00 US/Central"
        schedule = Schedule(
            timezone="US/Central",
            start_time='09:00',
            stop_time='17:00',
            restricted_days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Saturday', 'Sunday'],
            prohibited_days=['Friday']
        )
        with freezegun.freeze_time(string_to_date(test_date)):
            result = schedule.check_schedule()
        self.assertFalse(result)

    def test_outside3(self):
        test_date = "2024-05-03 12:00:00 US/Central"
        schedule = Schedule(
            assume='prohibited',
            timezone="US/Central",
            unrestricted_days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Saturday', 'Sunday'],
        )
        with freezegun.freeze_time(string_to_date(test_date)):
            result = schedule.check_schedule()
        self.assertFalse(result)

    def test_outside5(self):
        test_date = "2024-05-03 12:00:00 US/Central"
        schedule = Schedule(
            timezone="US/Central",
            unrestricted_days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            specific_dates=[
                    {
                        'start_date': '2024-05-03',
                        'stop_date': '2024-05-03',
                        'mode': 'prohibited'
                    },
                ]
        )
        with freezegun.freeze_time(string_to_date(test_date)):
            result = schedule.check_schedule()
        self.assertFalse(result)

    def test_outside6(self):
        test_date = "2024-05-03 12:00:00 US/Central"
        schedule = Schedule(
            timezone="US/Central",
            start_time='17:00',
            stop_time='09:00'
        )
        with freezegun.freeze_time(string_to_date(test_date)):
            result = schedule.check_schedule()
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
