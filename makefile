format:
	black *.py

test:
	make format
	python3 test.py