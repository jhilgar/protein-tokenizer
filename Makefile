ifneq ($(OS),Windows_NT)
	SHELL = /usr/bin/env bash -o pipefail
endif

default: help

.PHONY: help
help:
	@echo commands: install, test, and run [frontend, backend, dataanalyzer, datacollector]

.PHONY: install
install:
ifeq ($(OS),Windows_NT)
	python -m venv .venv && \
	.\.venv\Scripts\activate && \
	pip install -r requirements.txt
else
	python3 -m venv .venv && \
	source .venv/bin/activate && \
	pip install -r requirements.txt
endif
	cd ./applications/frontend && \
	npm install

.PHONY: test
test:
ifeq ($(OS),Windows_NT)
	.\.venv\Scripts\activate && \
	pytest
else
	source .venv/bin/activate && \
	pytest
endif

.PHONY: make run frontend
run frontend:
	cd ./applications/frontend && \
	npm run dev