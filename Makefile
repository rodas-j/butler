coverage:
	poetry run coverage run -m pytest -m "not prod" && poetry run coverage report -m

freeze:
	poetry export --without-hashes --format=requirements.txt > requirements.txt

dev:
	poetry run python main.py

build-docker:
	docker build . -f Dockerfile -t butler

test-dev:
	poetry run pytest -m "not prod"

test-prod:
	poetry run pytest -m "prod"
