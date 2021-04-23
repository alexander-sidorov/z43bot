format:
	isort --virtual-env=./.venv/ ./src ./tests
	black ./src ./tests


run-prod:
	uvicorn \
		z43bot.asgi:app \
		--host 0.0.0.0 \
		--lifespan off \
		--port $(PORT) \
		--workers 4 \
		--ws none \


run:
	python src/runner.py


qa: run-tests check-types check-imports check-code-style run-static-code-analysis
	@echo "quality is assured"


run-tests:
	coverage run -m pytest -vv
	coverage html
	coverage report


check-types:
	mypy --package z43bot


check-imports:
	isort --virtual-env=./.venv/ --check-only ./src ./tests


check-code-style:
	black --check ./src ./tests


run-static-code-analysis:
	flake8 \
		--show-source \
		--max-line-length=79 \
		./src/ \

	pylint z43bot


db:
	python -m db.migrations
