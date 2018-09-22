install:
	pip install -r requirements.dev.txt

test:
	cd play && ENV=local pytest

run:
	cd play && ENV=local ./manage.py runserver
