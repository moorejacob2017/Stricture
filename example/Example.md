# Stricture Example


## Why?
I come from a pentesting background. Tools such as Nessus, Nmap, and Masscan can take days to run with certain configurations and can impact network performance, take down services, etc. Therefore, it is common to have "safe" scanning hours and "unsafe" scanning hours. A client may want to have their unsafe scanning hours to be on the off-hours so that if something happens it does not impact the business. Others may want their unsafe hours to be during business hours so that if something goes wrong there are people there to fix it. Regardless of when the the unsafe hours are, it's always a pain having to start and stop things manually. So, I created this library to abstract the idea of starting and stopping things so people can easily make tools that start and stop things on a human readable schedule.

In this example, we will have a dummy API that will start and stop an operation based on the API calls. For a practical 1:1 comparison, this is analogous to running a Nessus Scan and using the Nessus API to pause and continue a network scan.

__NOTE:__ For another use case, strictures can also be applied to Nmap and Masscan processes, where the stricture sends SIGSTOPs and SIGCONTs to start and stop scanning without losing any progress. However, we will focus on the dummy API in this example. See the docs for `CommandStricture` and `ProcessesStricture` usages.


## A DummyAPI Example
To start, lets say we have a dummy API. Our API will create a process that slowly counts to 1,000,000. The api has 4 functions:
- `launch`
  - Starts a counting process in the background. Returns the ID used to manage the process.
  - `curl -X GET http://localhost:5000/api/launch`
- `pause`
  - Halts the counting process. Takes the process ID.
  - `curl -X POST -H "Content-Type: application/json" -d '{"process_id": "<process_id_here>"}' http://localhost:5000/api/pause`
- `resume` 
  - Continues the counting process. Takes the process ID.
  - `curl -X POST -H "Content-Type: application/json" -d '{"process_id": "<process_id_here>"}' http://localhost:5000/api/resume`
- `status`
  - Gets the status of the counting process. Takes the process ID.
  - `curl -X GET http://localhost:5000/api/status?process_id=<process_id_here>`

I've gone ahead and made the API in this example, which is in the [dummy_api.py](./dummy_api.py) file. It can be ran with `python3 dummy_api.py`.

Now lets say there is a python module that we can use for interacting with the dummy API. The module containts a class called `DummyAPIManager` that takes the API url upon instantiation and has the following methods:
- `api_launch` - calls the `launch` function on the API and saves the process ID.
- `api_pause` - calls the `pause` function on the API with the process ID.
- `api_resume` - calls the `resume` function on the API with the process ID.
- `api_is_alive` - calls the `status` function on the API with the process ID. Returns `True` if the counting process is still counting and `False` if done.

I've also made the `DummyAPIManager` class, which can be found in the the [dummy_manager.py](./dummy_manager.py) file.

## Applying a `Stricture` to the API
With a test case made and a way to interact with the DummyAPI, we can create and apply a `Stricture` to start and stop the counting process on the schedule that we provide. We do this by giving a `Schedule` to a `Stricture`, then providing it with the functions used to launch the process, stop the process, continue the process, and check if the process is still running. Then we just tell it to execute.

[example.py](./example.py)
```python

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
```

That's it! The `Stricture` will launch a counting process on the API when it is in schedule, then start and stop the counting process depending on if the current date and time is in or out of schedule.