.PHONY: all run test stddev clean help

all: run

run:
	python3 src/calc.py

test:
	.venv/bin/pytest -v src/test.py
stddev:
	python3 src/profiling.py
clean:
	rm -rf src/__pycache__ __pycache__
	rm -rf .pytest_cache

help:
	@echo "Dostupne cile:"
	@echo "  all    - Spusti aplikaci (stejne jako run)"
	@echo "  run    - Spusti kalkulacku"
	@echo "  test   - Spusti testy"
	@echo "  stddev - Spusti program pro smerodatnou odchylku"
	@echo "  clean  - Odstrani docasne soubory"