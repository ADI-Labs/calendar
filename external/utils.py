import itertools
from enum import Enum


class Constant(Enum):   # constant that is not equal to anything else
    null = 1


def grouper(iterable, n=50):
    "Collect data into fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    chunks = itertools.zip_longest(fillvalue=Constant.null, *args)

    return ((item for item in chunk if item is not Constant.null)
            for chunk in chunks)
