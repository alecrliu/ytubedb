ifeq ($(shell uname), Darwin)          # Apple
	PYTHON   := python3
	PIP      := pip3
	PYLINT   := pylint
	COVERAGE := coverage
	PYDOC    := python -m pydoc
	AUTOPEP8 := autopep8
else ifeq ($(shell uname -p), unknown) # Windows
	PYTHON   := python
	PIP      := pip3
	PYLINT   := pylint
	COVERAGE := coverage
	PYDOC    := python -m pydoc
	AUTOPEP8 := autopep8
else                                   # UTCS
	PYTHON   := python3
	PIP      := pip3
	PYLINT   := pylint3
	COVERAGE := coverage
	PYDOC    := pydoc3
	AUTOPEP8 := autopep8
endif

versions:
	$(PYTHON) --version
	$(PIP) --version
	$(PYLINT) --version
	$(COVERAGE) --version
	$(PYDOC) --version
	$(AUTOPEP8) --version

DB: database.py
	$(PYTHON) database.py

cleanCodePY: APIs.py models.py database.py test.py gitlabStats.py main.py
	$(AUTOPEP8) --in-place APIs.py
	$(AUTOPEP8) --in-place models.py
	$(AUTOPEP8) --in-place database.py
	$(AUTOPEP8) --in-place test.py
	$(AUTOPEP8) --in-place gitlabStats.py
	$(AUTOPEP8) --in-place main.py

# for some reason, error generating docs for flask_sqlalchemy
# models: models.py
# 	$(PYDOC) -w models > models.html

IDB2:
	git log > IDB2.log

IDB3:
	git log > IDB3.log