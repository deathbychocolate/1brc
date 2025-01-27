# 1brc
Welcome to the 1 billion row challenge!

Our intent is to use Python built-in libraries only. This would mean libraries such as `pandas`, `polars`, `numpy` or anything else that is not part of the standard Python install are not allowed.

## Challenge Description:
This is the challenge description as extracted from the original repo listed in the 'Relevant links' section.
> The task is to write a ~~Java~~ Python program which reads the file, calculates the min, mean, and max temperature value per weather station, and emits the results on stdout like this (i.e. sorted alphabetically by station name, and the result values per station in the format `<min>/<mean>/<max>`, rounded to one fractional digit):  
```{Abha=-23.0/18.0/59.2, Abidjan=-16.2/26.0/67.3, Abéché=-10.0/29.4/69.0, Accra=-10.1/26.4/66.4, Addis Ababa=-23.7/16.0/67.0, Adelaide=-27.8/17.3/58.5, ...}```

## Challenge Report:

All algorithms were initially ran against a smaller 805KB file in the data folder. 

### Version 1:
This file is not able to complete the challenge. The longest it was left to run was 30 mins and then we issued a `SIGINT` to stop.

The file was written with mindset of 'get a working algorithm, clean up inefficiencies later', as such the code assumes that we will enough memory to process **13GB** worth of CSV file as we please. This is not the case, not even for a **48GB** system.

### Version 2:
[placeholder]

### Version 3:
[placeholder]

### Version 4:
[placeholder]

## How do I run it?
In this project we use a Makefile that comes with a handy `help` target. Run `make help` to find the action you want to execute.

An example command would be `make run` to run version 1. To run anu other version use `make run VERSION=v2`. Note, all versions run against the **805KB** file located here -> `1brc/src/data/weather_stations.csv`. To change the file of choice you can run something similar to `make run VERSION=v2 FILEPATH=my_file_of_choice.txt`.

## Relevant links:
- The main repo with Java implemented solutions: `https://github.com/gunnarmorling/1brc`
- The main repo with Java implemented solutions (blogs): `https://github.com/gunnarmorling/1brc?tab=readme-ov-file#1brc-on-the-web`
- Other implementations in Python: `https://github.com/dougmercer-yt/1brc/tree/main`
