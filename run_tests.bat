call "./env/Scripts/activate"
python -m pytest --doctest-modules
flake8 pylookback
flake8 tests
