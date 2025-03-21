../../explorers/global-food.explorer.tsv: *.py *.csv *.tsv
	poetry env use 3.11
	poetry run pip install --upgrade pip setuptools wheel
	poetry run pip install --only-binary=numpy,pandas numpy pandas
	poetry install --no-root
	poetry run python global-food-explorer.py
