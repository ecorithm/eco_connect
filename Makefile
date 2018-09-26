.PHONY: docs

init:
	pip install pipenv --upgrade
	pipenv install --dev --skip-lock

test:
	coverage run -m pytest

publish:
	pip install 'twine>=1.5.0'
	python setup.py sdist
	twine upload dist/*
	rm -rf build dist .egg requests.egg-info

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"
