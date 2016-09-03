PACKAGENAME=ldapy

.PHONY: help
help:
	@echo 'Please use "make <target>" where <target> is one of'
	@echo "  release   - build a release and publish it"
	@echo "  dev       - prepare a development environment (includes tests)"
	@echo "  instdev   - prepare a development environment (no tests)"
	@echo "  install   - install into current Python environment"
	@echo "  test      - test from this directory using tox, including test coverage"
	@echo "  publish   - upload to PyPI"
	@echo "  clean     - remove any temporary build products"

.PHONY: release
release: publish
	@echo "$@ done."

.PHONY: dev
dev: instdev test
	@echo "$@ done."

.PHONY: instdev
instdev:
	pip install -r dev-requirements.txt
	python setup.py develop
	@echo "$@ done."

.PHONY: install
install:
	python setup.py install
	@echo "$@ done."

.PHONY: test
test:
	pip install 'tox>=1.7.2'
	tox
	@echo "$@ done."

.PHONY: publish
publish:
	python setup.py sdist upload
	@echo "$@ done; uploaded the package to PyPI."

.PHONY: clean
clean:
	find . -name "*pyc" | xargs -r rm
	rm -fr build $(PACKAGENAME).egg-info
	rm -fr __pycache__
	rm -fr .cache
	@echo "$@ done."