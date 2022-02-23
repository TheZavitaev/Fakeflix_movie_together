set_linters:
	echo "ставлю нужные библиотеки"
	pip install  wemake-python-styleguide flake8-html mypy lxml
	mypy --install-types

linters:
	echo "Запускаю isort"
	isort .
	echo "Запускаю flake8"
	flake8
	echo "Запускаю mypy"
	mypy api/src/*
	mypy etl/src/*
	mypy event_generator/*