.PHONY: format
format:
	isort --virtual-env=./.venv/ ./src ./tests
	black  ./src ./tests


.PHONY: run-prod
run-prod:
	uvicorn \
		z43bot.asgi:app \
		--host 0.0.0.0 \
		--lifespan off \
		--port $(PORT) \
		--workers 4 \
		--ws none \


.PHONY: run
run:
	python src/runner.py


.PHONY: qa
qa: run-tests check-types check-imports check-code-style run-static-code-analysis
	@echo "quality is assured"


.PHONY: run-tests
run-tests:
	coverage run -m pytest -vv
	coverage html
	coverage report


.PHONY: check-types
check-types:
	mypy --package z43bot


.PHONY: check-imports
check-imports:
	isort --virtual-env=./.venv/ --check-only ./src ./tests


.PHONY: check-code-style
check-code-style:
	black --check ./src ./tests


.PHONY: run-static-code-analysis
run-static-code-analysis:
	flake8 \
		--show-source \
		--max-line-length=79 \
		./src/ \

	pylint z43bot

