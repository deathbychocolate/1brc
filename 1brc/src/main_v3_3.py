"""The only file we will ever need."""

import multiprocessing
import sys
from mmap import ACCESS_READ, mmap
from os import cpu_count, environ
from timeit import timeit

filepath: str = environ["FILEPATH"]


def to_int(row: bytes) -> int:
    # Parse sign
    if row[0] == 45:  # ASCII for "-"
        sign = -1
        idx = 1
    else:
        sign = 1
        idx = 0
    # Check the position of the decimal point
    if row[idx + 1] == 46:  # ASCII for "."
        # -#.# or #.#
        # 528 == ord("0") * 11
        result = sign * ((row[idx] * 10 + row[idx + 2]) - 528)
    else:
        # -##.# or ##.#
        # 5328 == ord("0") * 111
        result = sign * ((row[idx] * 100 + row[idx + 1] * 10 + row[idx + 3]) - 5328)

    return result


def process_row(row: bytes, weather_station_data_chunk: dict[bytes, list]) -> None:
    """Processes each row of bytes in such that we avoid calling `mmap.mmap.readline()`
    and `list_object.append()`.

    This function is critical to this implementation working. Without it,
    our only other option is to use built-in python `mmap.mmap.readline()`
    or `list_object.append()`. Doing so with a multicore solution will consume **all** RAM
    within the first `~10 seconds` of program execution. This in turn causes the execution
    speed to slow to a crawl, returning us to the same set of issues in `v1`.

    But by processing each row "manually", we make tremendous gains.

    The rows processed here should look like the following:
        Bloemfontein;-1.3
        Austin;34.4
        Baltimore;2.3
        Bamako;19.7
        Cairns;23.3
        Pontianak;33.8
        Los Angeles;24.2
        Milan;25.0
        Pontianak;11.0
        Bratislava;2.4

    Args:
        row (bytes): A single row from the file containing the temperature data.
        weather_station_data_chunk (dict[bytes, list]): Where we store the row after processing.
            The key is the `city_name` and value is organized as follows:
                - First  item [0]: Number of occurrences.         (we use this to calculate the avg)
                - Second item [1]: Sum total of all temperatures. (we divide this item by the first)
                - Third  item [2]: The minimum temperature found.
                - Fourth item [3]: The maximum temperature found.
    """
    index_delim: int = row.find(b";")

    city_name: bytes = row[:index_delim]  # up to but not including ';'
    city_temperature: int = to_int(row[index_delim + 1 : -1])  # do not include ';' or '\n'.

    if city_name in weather_station_data_chunk:
        occur_total_min_max = weather_station_data_chunk[city_name]
        occur_total_min_max[0] += 1  # number occurrences
        occur_total_min_max[1] += city_temperature  # sum total temp
        occur_total_min_max[2] = min(occur_total_min_max[2], city_temperature)  # minimum temp found
        occur_total_min_max[3] = max(occur_total_min_max[3], city_temperature)  # maximum temp found
    else:  # initialize
        weather_station_data_chunk[city_name] = [
            1,
            city_temperature,
            city_temperature,
            city_temperature,
        ]


def process_chunk(start_byte: int, end_byte: int) -> dict[bytes, list[int]]:
    """Distribute the work to the worker and process all rows from `start_byte`
    to `end_byte`.

    Args:
        start_byte (int): Represents the beginning of the chunk.
        end_byte (int): Represents the end of the chunk. Usually a `\n`.

    Returns:
        dict[bytes, list[float]]: The now parsed data. The key is the `city_name`, the value is explained in `process_row()`.
    """
    weather_station_data_chunk: dict[bytes, list[int]] = {}
    with open(file=filepath, mode="rb") as fp:
        with mmap(fileno=fp.fileno(), length=end_byte, access=ACCESS_READ) as mfp:
            mfp.seek(start_byte)
            for row in iter(mfp.readline, b""):
                process_row(row, weather_station_data_chunk)

    return weather_station_data_chunk


def reduce_chunks(weather_station_data_chunks: list[dict[bytes, list[int]]]) -> dict[bytes, list[int]]:
    """Reduces the weather station chunks from being `1 list of dicts` to `1 dict`.
    This is needed in order for us to sort the solution later.

    Args:
        weather_station_data_chunks (list[dict[bytes, list[int]]]): Our parsed weather station data.

    Returns:
        dict[bytes, list[int]]: A reduced version of our `1 list of dicts`. It is now `1 dict`.
    """
    weather_station_data: dict[bytes, list[int]] = {}

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
    """This function has gotten much more complicated.

    The only difference with this version and `v3_2` is we added a custom `to_int()` function.
    The idea is floats in Python are expensive to do operations on. It would be much quicker
    to process integers. And considering most solutions to the `1brc` challenge only have
    `1` decimal point of accuracy, we can apply some trickery. And we only have to remember
    to multiply the final result by `0.1` to convert back to a float.

    I feel I should emphasize, full credit for `to_int()` goes to `Doug Mercer` who hosts the specific
    solution here: `https://github.com/dougmercer-yt/1brc/blob/c408f597d4a559db398805a49b70e5cba351e099/src/doug_booty4.py#L9`

    Thank you all for reading!
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
            total_bytes = len(mfp)
            start_byte = mfp.tell()
            bytes_per_core = total_bytes // core_count
            for _ in range(core_count):
                end_byte = min(start_byte + bytes_per_core, total_bytes)
                end_byte = mfp.find(b"\n", end_byte)
                end_byte = end_byte + 1 if end_byte != -1 else total_bytes  # do not go beyond the actual size of the file
                offsets.append((start_byte, end_byte))
                start_byte = end_byte

    weather_station_data_chunks: list[dict[bytes, list[int]]] = []
    with multiprocessing.Pool(processes=core_count) as pool:
        weather_station_data_chunks = pool.starmap(func=process_chunk, iterable=offsets)

    # reduce the data parsed by multiple workers from 1 list of dicts -> 1 dict
    weather_station_data: dict[bytes, list[int]] = reduce_chunks(weather_station_data_chunks)

    # now that the data is organized, process it to get min, mean, and max values
    weather_station_data_per_city: str = ", ".join(
        (
            f"{city_name.decode()}={0.1*occur_total_min_max[2]:.1f}/{0.1*(occur_total_min_max[1] / occur_total_min_max[0]):.1f}/{0.1*occur_total_min_max[3]:.1f}"
            for city_name, occur_total_min_max in sorted(weather_station_data.items())
        )
    )
    print("{", weather_station_data_per_city, "}", sep="")


def main() -> None:
    """Call this function to run the program."""
    # parse_weather_station_data()
    wall_time_in_seconds: float = timeit(
        stmt="parse_weather_station_data()",
        setup="from main_v3_3 import parse_weather_station_data",
        number=1,  # times we call the function
    )
    print(f"Wall time in seconds: {wall_time_in_seconds}")


if __name__ == "__main__":
    main()
