.DEFAULT_GOAL := help

MAKEFILE_PATH := $(shell readlink -f Makefile)

VERSION ?= v1## The version of the file we want to run (part of filename).

.PHONY: run
run: ## Run a 'main.py' file.
	@echo "Running: 1brc/src/main_${VERSION}.py"
	@python3 1brc/src/main_${VERSION}.py

.PHONY: profile
profile: ## Run a 'main.py' file with a profiler (Scalene).
	@echo "Running: 1brc/src/main_${VERSION}.py"
	@python3 -m scalene 1brc/src/main_${VERSION}.py

.PHONY: help
help: ## Show help and exit.
	@./scripts/help.sh $(MAKEFILE_PATH)
