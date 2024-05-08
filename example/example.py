
import logging
import stricture
from .dummy_manager import DummyAPIManager


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S %Z'
    )

    dummy = DummyAPIManager('http://127.0.0.1:5000/')


    # Off-hours Schedule:
    #   7:00pm-7:00am on weekdays
    #   All day on weekends
    schedule_dict = {
        'start_time':'19:00',
        'stop_time':'7:00',
        'unrestricted_days':[
            'Saturday',
            'Sunday'
        ]
    }

    schedule = stricture.Schedule.from_dict(schedule_dict)

    dummy_stricture = stricture.Stricture(schedule) # Initialize Stricture with schedule
    dummy_stricture.set_launch(dummy.api_launch) # Set how to launch the counting process
    dummy_stricture.set_pause(dummy.api_pause) # Set how to pause the counting process
    dummy_stricture.set_resume(dummy.api_resume) # Set how to resume the counting process
    dummy_stricture.set_is_alive(dummy.api_is_alive) # Set how to check if the counting process is still alive or completed

    dummy_stricture.execute() # Runs the counting process according the the schedule

    print('Done!')

if __name__ == "__main__":
    main()
