DEFAULT_INCHES: tuple[float, ...] = (1, 2, 3, 6, 12, 24, 36)
DEFAULT_FEET: tuple[float, ...] = (
    1,
    2,
    2.5,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    15,
    20,
    25,
    30,
    35,
    40,
    45,
    50,
    55,
    60,
    120,
)
DEFAULT_MILES: tuple[float, ...] = (0.25, 0.5, 1, 2, 3, 5, 10)
DEFAULT_POUNDS: tuple[float, ...] = (1, 2, 5, 10, 15, 20, 25, 50, 75, 100, 150, 200)


def inches_to_meters(inches: float) -> float:
    return inches * 0.0254


def feet_to_meters(feet: float) -> float:
    return feet * 0.3048


def miles_to_kilometers(miles: float) -> float:
    return miles * 1.609344


def pounds_to_grams(pounds: float) -> float:
    return pounds * 453.59237


def pounds_to_kilograms(pounds: float) -> float:
    return pounds_to_grams(pounds) / 1000


def inches_to_squares(inches: float) -> float:
    return inches / 60


def feet_to_squares(feet: float) -> float:
    return feet / 5


def miles_to_squares(miles: float) -> float:
    return miles * 1056


def sorted_unique(values: tuple[float, ...]) -> tuple[float, ...]:
    return tuple(sorted(set(values)))
