"""The only file we will ever need."""

from os import environ
from timeit import timeit
from mmap import mmap, ACCESS_READ

def parse_weather_station_data() -> None:
    """This function holds all the logic we need.

    This one is where the really big changes start to appear.
    We discover that there a package named `mmap`, which serves
    as an API for memory mapping in Python.

    Simply using an `mmap` pointer rather than the `open()` pointer,
    gives us up to a `15% speedup` compared to `v3`.

    At this point I felt confident enough that I was hitting the single
    core optimization limit and need to start leveraging multicore solutions;
    using this code as the foundation.
    """

    filepath: str = environ["FILEPATH"]
    weather_station_data: dict[bytes, list[float]] = {}
    with open(file=filepath, mode="rb") as fp:
        with mmap(fileno=fp.fileno(), length=0, access=ACCESS_READ) as m:
            for row in iter(m.readline, b""):
                city_name, city_temperature = row.rstrip().split(b";")
                if not weather_station_data.get(city_name):
                    weather_station_data[city_name] = [float(city_temperature)]
                else:
                    weather_station_data[city_name].append(float(city_temperature))

    # now that the data is organized, process it to get min, mean, and max values
    weather_station_data_per_city: str = ", ".join(
        (
            f"{city_name.decode()}={min(temperatures)}/{sum(temperatures) / len(temperatures)}/{max(temperatures)}"
            for city_name, temperatures in sorted(weather_station_data.items())
        )
    )
    print("{", weather_station_data_per_city, "}", sep="")


def main() -> None:
    """Call this function to run the program."""
    # parse_weather_station_data()
    wall_time_in_seconds: float = timeit(
        stmt="parse_weather_station_data()",
        setup="from main_v3_1 import parse_weather_station_data",
        number=1,  # times we call the function
    )
    print(f"Wall time in seconds: {wall_time_in_seconds}")


if __name__ == "__main__":
    main()
