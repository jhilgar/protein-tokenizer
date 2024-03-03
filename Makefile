ifneq ($(OS),Windows_NT)
	SHELL = /usr/bin/env bash -o pipefail
endif

default: help

.PHONY: help
help:
	@echo ---
	@echo commands: install, test/[unit, integration] or run/[frontend, backend, dataanalyzer, or datacollector]
	@echo ---
	@echo NOTE: backend, dataanalyzer, and datacollector should be running to run test/integration
	@echo ---

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

.PHONY: test/unit
test/unit:
ifeq ($(OS),Windows_NT)
	.\.venv\Scripts\activate && \
	pytest .\components
else
	source .venv/bin/activate && \
	pytest ./components
endif

.PHONY: test/integration
test/integration:
ifeq ($(OS),Windows_NT)
	.\.venv\Scripts\activate && \
	pytest .\applications
else
	source .venv/bin/activate && \
	pytest ./applications
endif

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
	uvicorn applications.dataanalyzer.main:app --host 0.0.0.0 --port 8080
else
	source .venv/bin/activate && \
	uvicorn applications.dataanalyzer.main:app --host 0.0.0.0 --port 8080
endif

.PHONY: make run/datacollector
run/datacollector:
ifeq ($(OS),Windows_NT)
	.\.venv\Scripts\activate && \
	uvicorn applications.datacollector.main:app --host 0.0.0.0 --port 8888
else
	source .venv/bin/activate && \
	uvicorn applications.datacollector.main:app --host 0.0.0.0 --port 8888
endif