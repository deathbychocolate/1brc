"""The only file we will ever need."""

from timeit import timeit
from os import environ

import polars as pl

pl.Config.set_streaming_chunk_size(8_000_000)


def parse_weather_station_data() -> None:
    """This function holds all the logic we need."""

    df = (
        pl.scan_csv(
            environ["FILEPATH"],
            separator=";",
            has_header=False,
            new_columns=["city", "value"],
        )
        .group_by("city")
        .agg(
            pl.min("value").alias("min"),
            pl.mean("value").alias("mean"),
            pl.max("value").alias("max"),
        )
        .sort("city")
        .collect(streaming=True)
    )

    print(
        "{",
        ", ".join(
            f"{data[0]}={data[1]:.1f}/{data[2]:.1f}/{data[3]:.1f}"
            for data in df.iter_rows()
        ),
        "}",
        sep="",
    )


def main() -> None:
    """Call this function to run the program."""
    # parse_weather_station_data()
    wall_time_in_seconds: float = timeit(
        stmt="parse_weather_station_data()",
        setup="from main_v6 import parse_weather_station_data",
        number=1,  # times we call the function
    )
    print(f"Wall time in seconds: {wall_time_in_seconds}")


if __name__ == "__main__":
    main()
