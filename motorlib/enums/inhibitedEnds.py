from enum import Enum


# Python 3.11 supports `StrEnum` that would make this a bit more concise to write
# https://docs.python.org/3/library/enum.html#enum.StrEnum
class InhibitedEnds(str, Enum):
    NEITHER = 'Neither'
    TOP = 'Top'
    BOTTOM = 'Bottom'
    BOTH = 'Both'
