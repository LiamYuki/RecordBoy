format:
	black *.py

test:
	make format
	pytest test.py