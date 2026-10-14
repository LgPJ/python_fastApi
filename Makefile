# Interpreter used only to create the venv: python3 on Linux/macOS, falls back to python.
BOOTSTRAP ?= $(shell command -v python3 || command -v python)
PY ?= .venv/bin/python

.PHONY: install migrate run test smoke check

install:  ## create venv and install dependencies
	$(BOOTSTRAP) -m venv .venv
	$(PY) -m pip install -r requirements-dev.txt

migrate:  ## apply DB migrations
	$(PY) -m alembic upgrade head

run: migrate  ## start API with auto-reload
	$(PY) -m uvicorn app.main:app --reload

test:  ## unit/integration tests (pytest, in-memory DB)
	$(PY) -m pytest -q

smoke:  ## end-to-end checks against a real running server (throwaway DB)
	scripts/smoke_test.sh

check: test smoke  ## run everything
