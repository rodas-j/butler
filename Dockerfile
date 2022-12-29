# syntax=docker/dockerfile:1
FROM python:3.8.2-slim-buster

WORKDIR /pybutler


RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
RUN pip install --user poetry
ENV PATH="${PATH}:/root/.local/bin"
# add and install python requirements
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install
# add app
COPY . .
# run server
CMD exec poetry run gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 main:app