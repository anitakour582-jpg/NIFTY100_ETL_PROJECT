install:
	pip install -r requirements.txt

run:
	python scripts/main.py

test:
	pytest

lint:
	flake8 .

format:
	black .	