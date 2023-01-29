## Freeze Requirements
```python
poetry export --without-hashes --format=requirements.txt > requirements.txt
```

```bash
docker build . -f Dockerfile -t butler
```

```bash
poetry run coverage run -m pytest -m "not prod" && poetry run coverage report -m
```