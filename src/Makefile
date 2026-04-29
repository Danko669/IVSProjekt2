##
# @file Makefile
# @author Libor Maška xmaskal00
# @date 2026-04-09


CALC = calc.py
TEST = test.py
PROF = profiling.py
DOXY = Doxyfile

PYTHON = python3
VENV = .venv
VENV_PY = $(VENV)/bin/python3
VENV_PIP = $(VENV)/bin/pip
VENV_PYTEST = $(VENV)/bin/pytest
VENV_PYINSTALLER = $(VENV)/bin/pyinstaller


REQS = ../requirements.txt
ARCHIVE = ../xbaloud00_xkralva00_xmaskal00.tar.gz
REPO = ../repo

.DEFAULT_GOAL := all
.PHONY: all env run test stddev clean help doc pack

all: env stddev

env:
	test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	$(VENV_PIP) install -r $(REQS)

run: env
	$(VENV_PY) $(CALC)

test: env
	$(VENV_PYTEST) -v $(TEST)

stddev: env
	$(VENV_PYINSTALLER) --onefile --name stddev --distpath . --workpath ../build $(PROF)
	
clean:
	rm -rf __pycache__ .pytest_cache $(VENV)
	rm -rf ../doc/html
	rm -rf ../build/ ../dist/ ../calc.spec calc.spec
	rm -f $(ARCHIVE) stddev stddev.spec
	
doc:
	doxygen $(DOXY)
	
pack: clean
	$(MAKE) doc
	mkdir -p $(REPO)
	cp -r ../.git ../.gitignore ../README.md ../requirements.txt ../src/ ../mockup/ ../plan/ ../profiling/ ../install/ ../manual.pdf ../hodnoceni.txt ../skutecnost.txt ../screenshot.png ../debugging.png $(PACK_DIR)/ 2>/dev/null || true
	tar -czvf $(ARCHIVE) -C .. doc/ install/ repo/
	rm -rf $(REPO)

help:
	@echo "Dostupne cile:"
	@echo "  all    - Pripravi prostredi a stahne zavislosti (nepousti aplikaci)"
	@echo "  run    - Pripravi prostredi a spusti kalkulacku"
	@echo "  test   - Spusti unit testy"
	@echo "  stddev - Pripravi prostredi a zkompiluje program pro smerodatnou odchylku"
	@echo "  clean  - Odstrani docasne soubory a vygenerovanou dokumentaci"
	@echo "  doc    - Vygeneruje programovou dokumentaci"
	@echo "  pack   - Zabali projekt do archivu pro odevzdani"