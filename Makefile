
ENV_NAME=iponweb_k9
ENV_FILE=environment.yml

environment.setup:
	conda env create -f $(ENV_FILE) --name $(ENV_NAME)

environment.export:
	conda env export --name $(ENV_NAME) > $(ENV_FILE)

tests:
	pytest test/test_auction.py

run:
	python src/main.py

