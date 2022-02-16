init::
	python -m pip install --upgrade pip
	python -m pip install pip-tools
	python -m piptools sync requirements/requirements.txt requirements/dev-requirements.txt
	python -m pre_commit install
	npm install

black:
	black .

black-check:
	black --check .

flake8:
	flake8 .

lint: black-check flake8

run::
	flask run

watch:
	npm run watch

upgrade-db:
	flask db upgrade

load-data:
	flask manage load-data

drop-data:
	flask manage drop-data
