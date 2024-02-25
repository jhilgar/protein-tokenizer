SHELL = /usr/bin/env bash -o pipefail

.PHONY: help
help:
	@sed -n '/^\([a-z][^:]*\).*/s//    make \1/p' $(MAKEFILE_LIST)

.PHONY: frontend/run
frontend/run:
	npm --prefix applications/frontend run dev