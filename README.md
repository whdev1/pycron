![banner](https://user-images.githubusercontent.com/90288849/151294853-2878a645-c480-472d-a9c2-24398d510059.jpg)

<div align="center">
    <em>
        A simple Python library providing cron functionality via the use of a single decorator.
    </em>
</div>

## Installation
The latest version of pycron may be installed via `pip` as follows:

```
pip install pycron
```

## Usage
The `pycron` module provides a `@cron` decorator that may be used to mark functions declared `async` as cron jobs. The decorator takes a croniter-style cron string as input to determine when the function should be executed. For example, the following `test` function would be automatically executed every 5 seconds:

```Python
from datetime import datetime
import pycron

@pycron.cron("* * * * * */5")
async def test(timestamp: datetime):
    print(f"test cron job running at {timestamp}")

if __name__ == '__main__':
    pycron.start()
```

All functions declared with the `@cron` decorator should take a single positional argument that will contain the current timestamp when the function is automatically invoked. Also note the usage of the `pycron.start()` method. This function signals that automated job scheduling and execution should begin and it should be invoked after all jobs have been declared.

For more information on the format of the cron strings that should be provided to the `@cron` decorator, please see the [croniter documentation on PyPI](https://pypi.org/project/croniter/).