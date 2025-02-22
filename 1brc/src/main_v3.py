"""The only file we will ever need."""

from os import environ
from timeit import timeit


def parse_weather_station_data() -> None:
    """This function holds all the logic we need.

    The differences between this file and `v2` are small but important.
    We have optimized the loop a little by removing the need for the extra
    use of `city_temperature`, and we switch out the `list comprehension` to
    using a combination of `join()` and a `generator comprehension`.
    The generator, especially, made a significant difference.

    Memory usage by these algorithms is still very high (averaging at a little over `23GB`),
    but Python's generators make the operations from `sorted()` to have a much smaller effect
    on memory compared to a list comprehension. In my case, I notices there is a steady and
    incremental increase in memory usage  up to `23GB` (via `activity monitor`) rather than a
    sharp increase to `23GB` that the list comprehension has.

    I am uncertain if this improvement will be as impactful on other systems.
    """

    filepath: str = environ["FILEPATH"]
    weather_station_data: dict[bytes, list[float]] = {}
    with open(file=filepath, mode="rb") as fp:
        for row in fp:
            city_name, city_temperature = row.rstrip().split(b";")
            if not weather_station_data.get(city_name):
                weather_station_data[city_name] = [float(city_temperature)]
            else:
                weather_station_data[city_name].append(float(city_temperature))

    # now that the data is organized, process it to get min, mean, and max values
    weather_station_data_per_city: str = ", ".join(
        (
            f"{city_name.decode()}={min(temperatures):.1f}/{sum(temperatures) / len(temperatures):.1f}/{max(temperatures):.1f}"
            for city_name, temperatures in sorted(weather_station_data.items())
        )
    )
    print("{", weather_station_data_per_city, "}", sep="")


def main() -> None:
    """Call this function to run the program."""
    # parse_weather_station_data()
    wall_time_in_seconds: float = timeit(
        stmt="parse_weather_station_data()",
        setup="from main_v3 import parse_weather_station_data",
        number=1,  # times we call the function
    )
    print(f"Wall time in seconds: {wall_time_in_seconds}")


if __name__ == "__main__":
    main()
