##
# @file Makefile
# @author Libor Maška xmaskal00
# @date 2026-04-09


CALC = calc.py
TEST = test.py
PROF = profiling.py
DOXY = Doxyfile
ARCHIVE = ../xbaloud00_xkralva00_xmaskal00.tar.gz

.DEFAULT_GOAL := all
.PHONY: all run test stddev clean help doc pack

all: env

env:
	test -d .venv || python3 -m venv .venv
	.venv/bin/pip install -r ../requirements.txt

run: env
	python3 $(CALC)

test: env
	.venv/bin/pytest -v $(TEST)

stddev: env
	python3 $(PROF)

clean:
	rm -rf __pycache__ .pytest_cache
	rm -rf ../doc/html
	rm -rf ../build/ ../dist/ ../calc.spec calc.spec
	rm -f $(ARCHIVE)
	
doc:
	doxygen $(DOXY)
	
pack: clean
	$(MAKE) doc
	mkdir -p ../repo
	cp -r ../.git ../.gitignore ../README.md ../requirements.txt ../src/ ../mockup/ ../plan/ ../profiling/ ../install/ ../manual.pdf ../hodnoceni.txt ../skutecnost.txt ../screenshot.png ../debugging.png ../repo/ 2>/dev/null || true
	tar -czvf $(ARCHIVE) -C .. doc/ install/ repo/
	rm -rf ../repo

help:
	@echo "Dostupne cile:"
	@echo "  all    - Pripravi prostredi a stahne zavislosti (nepousti aplikaci)"
	@echo "  run    - Pripravi prostredi a spusti kalkulacku"
	@echo "  test   - Spusti unit testy"
	@echo "  stddev - Pripravi prostredi a spusti program pro smerodatnou odchylku"
	@echo "  clean  - Odstrani docasne soubory a vygenerovanou dokumentaci"
	@echo "  doc    - Vygeneruje programovou dokumentaci"
	@echo "  pack   - Zabali projekt do archivu pro odevzdani"