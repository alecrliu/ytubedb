ifeq ($(shell uname), Darwin)          # Apple
	PYTHON   := python3
	PIP      := pip3
	PYLINT   := pylint
	COVERAGE := coverage
	PDOC     := python -m pdoc
	AUTOPEP8 := autopep8
else ifeq ($(shell uname -p), unknown) # Windows
	PYTHON   := python
	PIP      := pip3
	PYLINT   := pylint
	COVERAGE := coverage
	PDOC     := python -m pdoc
	AUTOPEP8 := autopep8
else                                   # UTCS
	PYTHON   := python3
	PIP      := pip3
	PYLINT   := pylint3
	COVERAGE := coverage
	PDOC     := pdoc3
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

cleanCodePY: youtubeData.py models.py database.py test.py gitlabStats.py main.py
	$(AUTOPEP8) --in-place youtubeData.py
	$(AUTOPEP8) --in-place models.py
	$(AUTOPEP8) --in-place database.py
	$(AUTOPEP8) --in-place test.py
	$(AUTOPEP8) --in-place gitlabStats.py
	$(AUTOPEP8) --in-place main.py
	$(AUTOPEP8) --in-place test.py

test: test.py
	$(PYTHON) test.py

# IDBs have been removed to prevent overwriting the logs
IDB1:
# 	git log > IDB1.log

IDB2:
# 	git log > IDB2.log

IDB3:
#	git log > IDB3.log

models: # unwanted website behavior
#	$(PDOC) --output-dir models models.py