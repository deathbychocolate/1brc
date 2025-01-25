.DEFAULT_GOAL := help

MAKEFILE_PATH := $(shell readlink -f Makefile) ## Makefile absolute path.

.PHONY: run
run: ## Run the 'main.py' file.
	@python3 1brc/src/main.py

.PHONY: profile
profile: ## Run the 'main.py' file with a profiler (Scalene).
	@python3 -m scalene 1brc/src/main.py

.PHONY: help
help: ## Show help and exit.
	@./scripts/help.sh $(MAKEFILE_PATH)
