OUTDIR  := build
PYTHON  ?= ../../.venv/bin/python
TECTONIC ?=

.PHONY: pdf figures clean

pdf: figures
	mkdir -p $(OUTDIR)
	cd $(OUTDIR) && $${TECTONIC:-$$(command -v tectonic 2>/dev/null || node /Users/rezarahimi/.codex/plugins/cache/openai-bundled/latex-tectonic/0.1.1/scripts/tectonic-path.mjs)} ../main.tex

# Figures are plotted from the committed artifacts under papers/unified-report/generated/,
# which the script parses rather than hard-coding; it fails loudly if a value is missing.
figures:
	$(PYTHON) figures/make_facct_figures.py

clean:
	rm -rf $(OUTDIR)
