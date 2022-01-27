import datetime
import math


def performance() -> str:
    start = datetime.datetime.now()
    compute(end=50_000_000)
    timetaken = datetime.datetime.now() - start
    return f'Finish in: {timetaken.total_seconds()} seconds.'

def compute(end: int, start: int = 1) -> None:
    pos = start
    factor = 1000 * 1000 # This variable is only to function spend time processing
    while pos < end:
        pos += 1
        math.sqrt((pos - factor) * (pos - factor))


if __name__ == '__main__':
    print(performance())

# Finish in: 12.397751 seconds.
# Finish in: 12.341079 seconds.