CALC = src/calc.py
TEST = src/test.py
PROF = src/profiling.py
DOXY = src/Doxyfile
ARCHIVE = xbaloud00_xkralva00_xmaskal00.tar.gz

DEFAULT_GOAL := all
.PHONY: all run test stddev clean help doc pack

all: env

env:
	test -d .venv || python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

run: env
	python3 $(CALC)

test: env
	.venv/bin/pytest -v $(TEST)

stddev: env
	python3 $(PROF)

clean:
	rm -rf src/__pycache__ __pycache__
	rm -rf .pytest_cache
	rm -rf doc/html doc/latex doc/xml
	rm -f $(ARCHIVE)
	
doc:
	doxygen $(DOXY)
	
pack: clean
	tar -czvf $(ARCHIVE) src/ doc/ install/ plan/ mockup/ profiling/ README.md .gitignore

help:
	@echo "Dostupne cile:"
	@echo "  all    - Pripravi prostredi a stahne zavislosti (nepousti aplikaci)"
	@echo "  run    - Pripravi prostredi a spusti kalkulacku"
	@echo "  test   - Spusti unit testy"
	@echo "  stddev - Pripravi prostredi a spusti program pro smerodatnou odchylku"
	@echo "  clean  - Odstrani docasne soubory a vygenerovanou dokumentaci"
	@echo "  doc    - Vygeneruje programovou dokumentaci"
	@echo "  pack   - Zabali projekt do archivu pro odevzdani"