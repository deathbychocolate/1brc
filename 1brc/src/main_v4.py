"""The only file we will ever need."""

from os import environ
from timeit import timeit
from bisect import bisect_left, bisect_right


def find_in_sorted_list(element: bytes, sorted_list: list) -> int:
    """Locate the leftmost value exactly equal to `element`."""
    # https://docs.python.org/3/library/bisect.html
    i = bisect_left(sorted_list, element)
    if i != len(sorted_list) and sorted_list[i] == element:
        return i
    return -1


def parse_weather_station_data() -> None:
    """This function holds all the logic we need.

    This function constructs a dictionary called 'weather_station_data'.
    The dictionary groups all temps together by city name where each city has
    all temperatures accumulated.
    """

    filepath: str = environ["FILEPATH"]
    weather_station_names: list[bytes] = []
    weather_station_temps: list[list[float]] = []

    # initiate the lists, this is needed to use bisect correctly later.
    # with open(file=filepath, mode="rb") as fp:
    #     row = next(fp)
    #     city_name, city_temperature = row.rstrip().split(b";")
    #     weather_station_names.append(city_name)
    #     weather_station_temps.append([float(city_temperature)])

    with open(file=filepath, mode="rb") as fp:
        next(fp)  # skip first line
        index: int = -1
        for row in fp:
            city_name, city_temperature = row.rstrip().split(b";")
            index = find_in_sorted_list(
                element=city_name,
                sorted_list=weather_station_names,
            )  # is the city already in the list?
            if index == -1:  # if city not found in list, add the city name and the temp
                insertion_index: int = bisect_right(weather_station_names, city_name)
                weather_station_names.insert(insertion_index, city_name)
                weather_station_temps.insert(insertion_index, [float(city_temperature)])
            else:  # add the temp only to the index found
                weather_station_temps[index].append(float(city_temperature))

    # now that the data is organized, process it to get min, mean, and max values
    weather_station_data_per_city: str = ", ".join(
        (
            f"{city_name.decode()}={min(temperatures)}/{sum(temperatures) / len(temperatures)}/{max(temperatures)}"
            for city_name, temperatures in zip(
                weather_station_names, weather_station_temps
            )
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
