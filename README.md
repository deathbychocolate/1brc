# 1brc
Welcome to the 1 billion row challenge!

This attempt at the 1brc was inspired by the creator and coordinator of the challenge [@gunnarmorling](https://github.com/gunnarmorling/), and by the attempt from [@dougmercer-yt](https://github.com/dougmercer-yt/).

## Challenge Description:
This is the challenge description as extracted from the original repo. The repo is listed in the 'Relevant links' section.
> The task is to write a ~~Java~~ Python program which reads the file, calculates the min, mean, and max temperature value per weather station, and emits the results on stdout like this (i.e. sorted alphabetically by station name, and the result values per station in the format `<min>/<mean>/<max>`, rounded to one fractional digit):  
```{Abha=-23.0/18.0/59.2, Abidjan=-16.2/26.0/67.3, Abéché=-10.0/29.4/69.0, Accra=-10.1/26.4/66.4, Addis Ababa=-23.7/16.0/67.0, Adelaide=-27.8/17.3/58.5, ...}```

## Why can you learn from this repo?
You can expect to learn how to push pure Python implementations to their limit. You will definitely learn something if you have a situation similar to `1brc`:
- You have a very large file (`13GB` or more) stored on disk.
- The file is ready to process (no major transformations needed).
- You need to optimize using Python's multiprocessing module but are not getting expected results.
- You do not have the ability to use third party libraries (such as `Pandas` or `Polars`).

## Challenge Summary Report:
The following context is needed to understand the report completely:
- The data was collected on a M4 Pro MBP laptop. It had `14 CPU Cores` and `48GB` of RAM.
- The laptop was always plugged in, fully charged, and never had other applications running.
- The laptop generally ran at `~7-8 Watts` with nothing else running.
- The algorithms are running about `5-10% slower` than usual. This may be due to not doing a cold boot.
- All algorithms are CPU bound.
- All algorithms use a pure Python approach (except the ones specified).
- All versions' runtimes were generated at least once before starting measurements.
- All versions' runtimes were generated a minimum of 5 times (not including the first) to compute an average.
- And lastly the Python version of our CPython runs is `3.12.7`.

### Runtimes in seconds:
| Versions | Pypy3.10 (s)    | CPython (s)       | CPython + Scalene (s) | Third Party Libraries? |
| -------- | --------------- | ----------------- | --------------------- | ---------------------- |
|    v1    | Not determined  | Not determined    | Not determined        | No                     |
|    v2    | 113.96          |                   |                       | No                     |
|    v3    | 114.39          |                   |                       | No                     |
|    v3_1  |  99.01          | 297,83            |                       | No                     |
|    v3_2  |   7.75          |  34.01            |  53.53                | No                     |
|    v3_3  |   5.15          |  44.31            |  77.53                | No                     |
|    v4    | 166.54          |                   |                       | No                     |
|    v5    | Not determined  | 104.85            | 107.39                | Yes (Pandas)           |
|    v6    | Not determined  |   7.56            |  10.57                | Yes (Polars)           |

### Average Recorded Power Consumption in Watts (Approximation):
| Versions | Pypy3.10 (W)    | CPython (W)       | CPython + Scalene (W) | Third Party Libraries? |
| -------- | --------------- | ----------------- | --------------------- | ---------------------- |
|    v1    | Not determined  | Not determined    | Not determined        | No                     |
|    v2    | 21              |                   |                       | No                     |
|    v3    | 19              |                   |                       | No                     |
|    v3_1  | 19              | 22.5              |  24.5                 | No                     |
|    v3_2  | 85              | 90.0              |  80.0                 | No                     |
|    v3_3  | 82              | 90.0              |  80.0                 | No                     |
|    v4    | 18.5            |                   |                       | No                     |
|    v5    | Not determined  | 21.5              |  21.0                 | Yes (Pandas)           |
|    v6    | Not determined  | 63.0              |  54.5                 | Yes (Polars)           |

## How do I run it?
In this project we use a Makefile that comes with a handy `help` target. Run `make help` to find the action you want to execute.

If you prefer to copy paste commands, here are a few examples:  
`make run`  
`make profile`  
`make run FILEPATH=measurements.txt VERSION=v1 INTERPRETER=python3`  
`make run FILEPATH=measurements.txt VERSION=v2 INTERPRETER=python3`  
`make run FILEPATH=measurements.txt VERSION=v3 INTERPRETER=pypy3.10`  
`make run FILEPATH=measurements.txt VERSION=v3_1 INTERPRETER=pypy3.10`  
`make profile FILEPATH=measurements.txt VERSION=v3_1 INTERPRETER=python3`  

Please note:
- The `measurements.txt` file needs to be generated by yourself. I will not attempt to see if 1 billion rows of data (13GB) is something that Github allows us to add.
- This repo does not include dependencies. You must install `Scalene`, `Pandas`, and `Polars` yourself.
- Profiling uses `Scalene`, which is built to work with `CPython` only. As such, use `INTERPRETER=python3` for `make profile`. The same applies to `Pandas` and `Polars`.

## Relevant links:
- The main repo with Java implemented solutions: [https://github.com/gunnarmorling/1brc](https://github.com/gunnarmorling/1brc)
- The main repo with Java implemented solutions (blogs): [https://github.com/gunnarmorling/1brc?tab=readme-ov-file#1brc-on-the-web](https://github.com/gunnarmorling/1brc?tab=readme-ov-file#1brc-on-the-web)
