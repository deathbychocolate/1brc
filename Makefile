.DEFAULT_GOAL := help

MAKEFILE_PATH := $(shell readlink -f Makefile)

VERSION ?= v1## The version of main.py we want to run.
FILEPATH ?= 1brc/src/data/weather_stations.csv## The filepath of weather station data.

.PHONY: run
run: ## Run main.py.
	@echo "Running: 1brc/src/main_${VERSION}.py"
	@export FILEPATH=${FILEPATH} && python3 1brc/src/main_${VERSION}.py

.PHONY: profile
profile: ## Run main.py with a profiler (Scalene).
	@echo "Running: 1brc/src/main_${VERSION}.py"
	@export FILEPATH=${FILEPATH} && python3 -m scalene 1brc/src/main_${VERSION}.py

.PHONY: help
help: ## Show help and exit.
	@./scripts/help.sh $(MAKEFILE_PATH)
