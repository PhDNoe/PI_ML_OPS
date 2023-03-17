from enum import Enum

class PlatformOptions(str, Enum):
    disney = "disney"
    netflix = "netflix"
    amazon = "amazon"
    hulu = "hulu"
    Disney = "Disney"
    Netflix = "Netflix"
    Amazon = "Amazon"
    Hulu = "Hulu"


class DurationOptions(str, Enum):
    min = "min"
    seasons = "seasons"
    Min = "Min"
    Seasons = "Seasons"
    MIn = "MIN"
    SEsons = "SEASONS"
