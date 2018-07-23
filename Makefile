venv:
	virutalenv -p python3 venv

.PHONY: install
install:
	pip install -r requirements.txt


.env.yaml:
	./setup.sh

build: .env.yaml venv install

