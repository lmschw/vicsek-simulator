from enum import Enum

"""
Indicates the type of thresholding to use to determine if an individual particle should switch its value
"""
class ThresholdType(str, Enum):
    TWO_THRESHOLDS = "tt",
    SINGLE_DIFFERENCE_THRESHOLD = "sdt",
    TWO_THRESHOLDS_SIMPLE = "tts",
    TWO_THRESHOLDS_SIMPLE_REVERSE = "ttsr",
    HYSTERESIS = "hst",
    HYSTERESIS_REVERSED = "hstr"