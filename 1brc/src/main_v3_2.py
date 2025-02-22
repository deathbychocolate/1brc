"""The only file we will ever need."""

from os import environ
from timeit import timeit
from mmap import mmap, ACCESS_READ
import multiprocessing
from os import cpu_count
import sys

filepath: str = environ["FILEPATH"]

def process_row(row: bytes, weather_station_data_chunk: dict) -> None:
    index_delim: int = row.find(b";")

    city_name: bytes = row[:index_delim]
    city_temperature: float = float(row[index_delim + 1 : -1])  # do not include ';' or '\n'.

    if city_name in weather_station_data_chunk:
        occur_total_min_max = weather_station_data_chunk[city_name]
        occur_total_min_max[0] += 1  # number of city occurrences
        occur_total_min_max[1] += city_temperature  # total temp -> to generate avg temperature when by number of city occurrences.
        occur_total_min_max[2] = min(occur_total_min_max[2], city_temperature)  # minimum temp found
        occur_total_min_max[3] = max(occur_total_min_max[3], city_temperature)  # maximum temp found
    else:  # initialize
        weather_station_data_chunk[city_name] = [
            1,
            city_temperature,
            city_temperature,
            city_temperature,
        ]


def process_chunk(start_byte: int, end_byte: int) -> dict[bytes, list[float]]:
    weather_station_data_chunk: dict[bytes, list[float]] = {}
    with open(file=filepath, mode="rb") as fp:
        with mmap(fileno=fp.fileno(), length=end_byte, access=ACCESS_READ) as mfp:
            mfp.seek(start_byte)
            print(f"Started work on byte range -> ({start_byte}, {end_byte})")
            for row in iter(mfp.readline, b""):
                process_row(row, weather_station_data_chunk)

    return weather_station_data_chunk


def reduce_chunks(weather_station_data_chunks: list[dict[bytes, list[float]]]) -> dict[bytes, list[float]]:
    weather_station_data: dict[bytes, list[float]] = {}

    for parsed_data in weather_station_data_chunks:
        for city_name, occur_total_min_max_from_chunks in parsed_data.items():
            if city_name in weather_station_data:
                occur_total_min_max = weather_station_data[city_name]
                occur_total_min_max[0] += occur_total_min_max_from_chunks[0]
                occur_total_min_max[1] += occur_total_min_max_from_chunks[1]
                occur_total_min_max[2] = min(occur_total_min_max[2], occur_total_min_max_from_chunks[2])
                occur_total_min_max[3] = max(occur_total_min_max[3], occur_total_min_max_from_chunks[3])
            else:  # initialize
                weather_station_data[city_name] = occur_total_min_max_from_chunks

    return weather_station_data


def parse_weather_station_data() -> None:
    """This function holds all the logic we need.

    This function constructs a dictionary called `weather_station_data`.
    The dictionary groups all temps together by city name where each city has
    all temperatures accumulated.
    """

    # Count number of cores. Must be int to continue.
    temp: int | None = cpu_count()
    if temp is None:
        sys.exit(1)

    core_count: int = temp  # to fix mypy issues with passing int | None

    # Determine the offsets (start_byte and end_byte for each CPU core to work on).
    offsets: list[tuple[int, int]] = []
    with open(filepath, mode="rb") as fp:
        with mmap(fileno=fp.fileno(), length=0, access=ACCESS_READ) as mfp:
            length = len(mfp)
            start_byte = mfp.tell()
            bytes_per_core = len(mfp)//core_count
            for _ in range(core_count):
                end_byte = min(start_byte + bytes_per_core, length)
                end_byte = mfp.find(b"\n", end_byte)
                end_byte = end_byte + 1 if end_byte != -1 else length  # do not go beyond the actual size of the file
                offsets.append((start_byte, end_byte))
                start_byte = end_byte

    weather_station_data_chunks: list[dict[bytes, list[float]]] = []
    with multiprocessing.Pool(processes=core_count) as pool:
        weather_station_data_chunks = pool.starmap(func=process_chunk, iterable=offsets)

    # reduce the data parsed by multiple workers from 1 list of dicts -> 1 dict
    weather_station_data = reduce_chunks(weather_station_data_chunks)

    # now that the data is organized, process it to get min, mean, and max values
    weather_station_data_per_city: str = ", ".join(
        (
            f"{city_name.decode()}={occur_total_min_max[2]:.1f}/{(occur_total_min_max[1] / occur_total_min_max[0]):.1f}/{occur_total_min_max[3]:.1f}"
            for city_name, occur_total_min_max in sorted(weather_station_data.items())
        )
    )
    print("{", weather_station_data_per_city, "}", sep="")


def main() -> None:
    """Call this function to run the program."""
    # parse_weather_station_data()
    wall_time_in_seconds: float = timeit(
        stmt="parse_weather_station_data()",
        setup="from main_v3_2 import parse_weather_station_data",
        number=1,  # times we call the function
    )
    print(f"Wall time in seconds: {wall_time_in_seconds}")


if __name__ == "__main__":
    main()
