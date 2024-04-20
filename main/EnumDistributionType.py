from enum import Enum

class DistributionType(str, Enum):
    GLOBAL = "G",
    LOCAL_SINGLE_SITE = "LSS",
    LOCAL_MULTI_SITE = "LMS"