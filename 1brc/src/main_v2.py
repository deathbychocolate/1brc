"""The only file we will ever need."""

from os import environ
from timeit import timeit


def parse_weather_station_data() -> None:
    """This function holds all the logic we need.

    We have made significant improvements here compared to `v1`.
    We will not include all of them here, in fact you are better off
    doing a straight file diff with `v1`. But I will mention some:
        - We have stopped creating new variables in loops.
        - We have change the `open()` read mode from `r` to `rb`.
        - We have removed some unnecessary variables thus freeing up memory.
        - We are also a little bit smarter with joining the data.
    """

    filepath: str = environ["FILEPATH"]
    weather_station_data: dict[bytes, list[float]] = {}
    with open(file=filepath, mode="rb") as fp:
        for row in fp:
            city_name, city_temperature = row.split(b";")
            city_temperature = city_temperature.rstrip()
            if weather_station_data.get(city_name) is None:
                weather_station_data[city_name] = [float(city_temperature)]
            else:
                weather_station_data[city_name].append(float(city_temperature))

    # now that the data is organized, process it to get min, mean, and max values
    weather_station_data_per_city = [
        f"{city_name.decode()}={min(temperatures):.1f}/{sum(temperatures) / len(temperatures):.1f}/{max(temperatures):.1f}"
        for city_name, temperatures in sorted(weather_station_data.items())
    ]
    output: str = ", ".join(weather_station_data_per_city)
    print("{", output, "}", sep="")


def main() -> None:
    """Call this function to run the program."""
    # parse_weather_station_data()
    wall_time_in_seconds: float = timeit(
        stmt="parse_weather_station_data()",
        setup="from main_v2 import parse_weather_station_data",
        number=1,  # times we call the function
    )
    print(f"Wall time in seconds: {wall_time_in_seconds}")


if __name__ == "__main__":
    main()
