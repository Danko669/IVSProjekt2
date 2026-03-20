all: run

run:
	python3 src/calc.py

test:
	.venv/bin/pytest -v src/test.py
stddev:
	python3 src/profiling.py