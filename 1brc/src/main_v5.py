"""The only file we will ever need."""

from timeit import timeit
from os import environ

import pandas as pd


def parse_weather_station_data() -> None:
    """This function holds all the logic we need."""

    df = pd.read_csv(
        environ["FILEPATH"],
        sep=";",
        header=None,
        names=["station", "measure"],
    )
    df = df.groupby("station").agg(["min", "max", "mean"])
    df = df.sort_values("station")

    # fmt: off
    print(
        "{",
        ", ".join(
            (
                f"{row[0]}={row[1]}/{row[2]}/{row[3]}"
                for row in df.itertuples()
            )
        ),
        "}",
        sep="",
    )
    # fmt: on


def main() -> None:
    """Call this function to run the program."""
    # parse_weather_station_data()
    wall_time_in_seconds: float = timeit(
        stmt="parse_weather_station_data()",
        setup="from main_v5 import parse_weather_station_data",
        number=1,  # times we call the function
    )
    print(f"Wall time in seconds: {wall_time_in_seconds}")


if __name__ == "__main__":
    main()
