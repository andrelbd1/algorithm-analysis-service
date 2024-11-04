clean:
	@echo "Execute cleaning ..."
	find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
	rm -f coverage.xml

pep8:
	@find ./src -type f -not -name "*manager.py*" -not -path "*./.venv/*" -name "*.py"|xargs flake8 --max-line-length=130 --ignore=E402 --max-complexity=15

tests: clean pep8
	py.test tests --cov=src

test-coverage:clean pep8
	py.test --cov=src --cov-report=xml tests

test-sonar: test-coverage
	sonar-scanner -Dsonar.sources=.

test-sonar-local: test-coverage
	sonar-scanner -Dproject.settings=sonar-project-local.properties

migration-up:
	alembic -c alembic.ini upgrade head

migration-down:
	alembic -c alembic.ini downgrade -1
