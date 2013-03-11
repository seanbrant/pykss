develop:
	pip install "file://`pwd`#egg=pykss[tests]"
	pip install -e . --use-mirrors

lint:
	@echo "Linting Python files"
	flake8 --ignore=E501,E225,E121,E123,E124,E125,E127,E128 pykss
	@echo ""

install-test-requirements:
	pip install "file://`pwd`#egg=pykss[tests]"

test-python:
	@echo "Running Python tests"
	python setup.py -q test || exit 1
	@echo ""

test: install-test-requirements lint test-python
