.DEFAULT_GOAL := help

MAKEFILE_PATH := $(shell readlink -f Makefile) ## Makefile absolute path.

.PHONY: run
run: ## Run the 'main.py' file.
	@python3 1brc/src/main.py

.PHONY: test
test: ## Run the 'main.py' file.
	@python3 -m pytest 1brc/src/**.py

.PHONY: help
help: ## Show help and exit.
	@./scripts/help.sh $(MAKEFILE_PATH)
