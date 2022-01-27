import asyncio
from croniter import croniter
from dataclasses import dataclass
from datetime import datetime
from threading import Thread
import time
from types import FunctionType
from typing import (
    Any,
    List
)

# a class that wraps an individual function in a thread and calls it
class FunctionThread(Thread):
    function: FunctionType
    running: bool = False

    def __init__(self, function: FunctionType) -> None:
        super().__init__()
        self.function = function
    
    def run(self):
        self.running = True
        asyncio.run(self.function(datetime.now()))
        self.running = False

# define a boolean that represents whether or not the executor should
# continue running or not
_running: bool = False

# define a named tuple to represent an individual function and the time it has 
# been scheduled for. also keep track of the last time the function ran
@dataclass
class ScheduledFunc:
    function: FunctionType
    cron_str: str
    last_run: str

running_functions: List[FunctionThread] = []
scheduled_functions: List[ScheduledFunc] = []

def _add_scheduled_func(function_def: FunctionType, cron_str: str) -> None:
    global scheduled_functions

    scheduled_functions.append(
        ScheduledFunc(
            function_def,
            cron_str,
            datetime.utcnow().timestamp()
        )
    )

def cron(cron_str: str) -> None:
    # we don't actually need to wrap the function, so just return it from
    # this inner decorator function.
    def decorator(function_def: FunctionType) -> Any:
        # add this new function to the schedule
        _add_scheduled_func(function_def, cron_str)

        return function_def

    # return the wrapping decorator function
    return decorator

def start() -> None:
    global _running, scheduled_functions, running_functions

    # set the running flag to True and loop through starting the functions
    # according to their timestamps
    _running = True
    while _running:
        start_time: float = time.time()

        for scheduled_function in scheduled_functions:
            # instantiate a datetime representing the last time the function ran
            last_run: datetime = datetime.fromtimestamp(scheduled_function.last_run)

            # determine the next time the function should run as specified by its cron string
            next_run_timestamp: int = croniter(scheduled_function.cron_str, last_run).get_next(float)
            
            # check if the function should run based on whether or not the current timestamp
            # meets or exceeds the next run timestamp
            current_timestamp: float = datetime.now().timestamp()
            if current_timestamp >= next_run_timestamp:
                # execute a new instance of the job function and add it to the queue
                running_functions.append(
                    FunctionThread(
                        scheduled_function.function
                    )
                )
                running_functions[-1].start()

                # set the last run timestamp of this function to the current UTC time
                scheduled_function.last_run = datetime.utcnow().timestamp()
        
        # remove any threads that are done
        for n in range(len(running_functions) - 1, -1, -1):
            if not running_functions[n].running:
                del running_functions[n]
            
        # sleep so that this method only pulses every 1 second at the most
        end_time: float = time.time()
        if end_time - start_time < 1.0:
            time.sleep(1 - (end_time - start_time))
    
    # join all of the threads that we've created until they're done
    for n in range(len(running_functions) - 1, -1, -1):
        if not running_functions[n].running:
            del running_functions[n]
        else:
            running_functions[n].join()
            del running_functions[n]

def stop() -> None:
    global _running
    _running = False