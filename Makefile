
ENV_NAME=iponweb_k9
ENV_FILE=env.yml

environment.export:
	conda env export --name $(ENV_NAME) > $(ENV_FILE)


tests:
	pytest test/test_auction.py

run:
	python src/main.py

