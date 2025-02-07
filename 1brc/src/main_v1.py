"""The only file we will ever need."""

from os import environ
from timeit import timeit


def parse_weather_station_data() -> None:
    """This function holds all the logic we need.

    The thought was this algorithm would take about 20 mins
    on my home system. In the end goes north of 40 mins until we `SIGINT` it.
    Meaning, we decided the algorithm can not complete the task on a 13GB
    file. This is due to hitting our RAM limit.

    The algorithm quickly goes from 13GB to 26GB without releasing the memory
    to Heap. So, when we attempt to allocate another 13GB, it crawls to a halt.
    The problem is we wanted to get a working algorithm first (which is correct),
    without considering the size of the data.
    Version `V2` makes many improvements in the areas of memory and compute time.
    """
    filepath: str = environ["FILEPATH"]
    with open(file=filepath, mode="r", encoding="utf8") as fp:
        rows: list[str] = fp.read().splitlines()
        rows = sorted(rows)  # sort with O(nlog(n)) algorithm

        # Construct a dictionary 'weather_station_data' so that we group all temps together by city.
        # The city name is the key, the value is a list of floats.
        # Do all conversions needed.
        weather_station_data: dict[str, list[float]] = {}
        for row in rows:
            left: str = ""
            right: str = ""
            left, right = row.split(";", maxsplit=1)
            city_name: str = left
            city_temperature: float = float(right)
            if weather_station_data.get(city_name) is None:
                weather_station_data[city_name] = []
                weather_station_data[city_name].append(city_temperature)
            else:
                weather_station_data[city_name].append(city_temperature)

        # now that the data is organized, process it to get min, mean, and max values
        weather_station_data_processed: str = "{"
        temperatures: list[float]
        mean: float = -999.9
        minimum: float = -999.9
        maximum: float = -999.9
        for city_name, temperatures in weather_station_data.items():
            mean = sum(temperatures) / len(temperatures)
            minimum = min(temperatures)
            maximum = max(temperatures)
            weather_station_data_processed += (
                city_name
                + "="
                + "/".join([str(minimum), str(mean), str(maximum)])
                + ", "
            )

        weather_station_data_processed = weather_station_data_processed.rstrip(", ")
        weather_station_data_processed += "}"

        print(weather_station_data_processed)


def main() -> None:
    """Call this function to run the program."""
    # parse_weather_station_data()
    wall_time_in_seconds: float = timeit(
        stmt="parse_weather_station_data()",
        setup="from main_v1 import parse_weather_station_data",
        number=1,  # times we call the function
    )
    print(f"Wall time in seconds: {wall_time_in_seconds}")


if __name__ == "__main__":
    main()
