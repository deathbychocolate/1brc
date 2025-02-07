include .env

.DEFAULT_GOAL := help

MAKEFILE_PATH := $(shell readlink -f Makefile)
VERSION ?= ${VERSION}## The version of main.py we want to run (set in .env).
FILEPATH ?= ${FILEPATH}## The filepath of weather station data (set in .env).
INTERPRETER ?= ${INTERPRETER}## The interpreter of choice (set in .env) [python3|pypy3.10].

.PHONY: run
run: ## Run main.py.
	@echo "Running: 1brc/src/main_${VERSION}.py on ${FILEPATH} with ${INTERPRETER}."
	@export FILEPATH=${FILEPATH} && ${INTERPRETER} 1brc/src/main_${VERSION}.py

.PHONY: profile
profile: ## Run main.py with a profiler (Scalene).
	@echo "Profiling: 1brc/src/main_${VERSION}.py on ${FILEPATH} with ${INTERPRETER}."
	@export FILEPATH=${FILEPATH} && ${INTERPRETER} -m scalene 1brc/src/main_${VERSION}.py

.PHONY: help
help: ## Show help and exit.
	@./scripts/help.sh $(MAKEFILE_PATH)
