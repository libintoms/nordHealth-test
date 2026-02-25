PYTHON := .venv/bin/python
PYTEST := .venv/bin/pytest

.PHONY: venv install browsers test test-headed test-ui report

venv:
	python3 -m venv .venv

install: venv
	$(PYTHON) -m pip install -r requirements.txt

browsers:
	$(PYTHON) -m playwright install chromium

test:
	$(PYTEST)

test-headed:
	$(PYTEST) --headed

test-ui:
	PWDEBUG=1 $(PYTEST) --headed --slowmo 300

report:
	open reports/report.html
