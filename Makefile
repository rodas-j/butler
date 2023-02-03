coverage:
	poetry run coverage run -m pytest -m "not prod" && poetry run coverage report -m

freeze:
	poetry export --without-hashes --format=requirements.txt > requirements.txt

dev:
	poetry run python main.py

docker:
	docker build . -f Dockerfile -t butler
