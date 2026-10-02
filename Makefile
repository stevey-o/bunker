PY := .venv/bin/python
S  := scripts_code

.PHONY: all setup sync render drawings reports docs validate clean

all: sync render drawings reports docs validate

setup:
	python3 -m venv .venv
	$(PY) -m pip install -q --upgrade pip reportlab

sync:
	$(PY) $(S)/sync_config.py

render: sync
	$(PY) $(S)/render_all.py

drawings: render
	$(PY) $(S)/export_drawings.py

reports: render
	$(PY) $(S)/generate_bom.py
	$(PY) $(S)/generate_cutlist.py
	$(PY) $(S)/generate_weight_report.py
	$(PY) $(S)/generate_cost_report.py
	$(PY) $(S)/generate_fit_study.py

docs: sync
	$(PY) $(S)/generate_dimension_docs.py

validate:
	$(PY) $(S)/validate_model.py

clean:
	rm -rf output
