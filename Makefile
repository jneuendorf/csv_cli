.PHONY: test unittest e2e_test

test: unittest e2e_test

unittest:
	pipenv run python -m unittest

e2e_test:
	./e2e_test.sh
