## Freeze Requirements
```python
poetry export --without-hashes --format=requirements.txt > requirements.txt
```

```bash
docker build . -f Dockerfile -t helloworld
```