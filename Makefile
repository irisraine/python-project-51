install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8 page_loader

tests:
	poetry run pytest

coverage:
	poetry run pytest --cov=page_loader tests/ --cov-report xml

page-loader:
	poetry run page-loader
