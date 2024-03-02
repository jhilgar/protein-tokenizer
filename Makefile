ifneq ($(OS),Windows_NT)
	SHELL = /usr/bin/env bash -o pipefail
endif

default: help

.PHONY: help
help:
	@echo commands: install, test/ or run/[frontend, backend, dataanalyzer, or datacollector]

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

.PHONY: test/dataanalyzer
test/dataanalyzer:
ifeq ($(OS),Windows_NT)
	.\.venv\Scripts\activate && \
	pytest .\components\data_analyzer_test.py
else
	source .venv/bin/activate && \
	pytest ./components/data_analyzer_test.py
endif

.PHONY: test
test: test/dataanalyzer

.PHONY: make run/frontend
run/frontend:
	cd ./applications/frontend && \
	npm run dev

.PHONY: make run/backend
run/backend:
ifeq ($(OS),Windows_NT)
	.\.venv\Scripts\activate && \
	uvicorn applications.backend.main:app --host 0.0.0.0 --port 8000
else
	source .venv/bin/activate && \
	uvicorn applications.backend.main:app --host 0.0.0.0 --port 8000
endif

.PHONY: make run/dataanalyzer
run/dataanalyzer:
ifeq ($(OS),Windows_NT)
	.\.venv\Scripts\activate && \
	uvicorn applications.dataanalyzer.main:app --host 0.0.0.0 --port 8000
else
	source .venv/bin/activate && \
	uvicorn applications.dataanalyzer.main:app --host 0.0.0.0 --port 8000
endif

