.PHONY: all clean check format test lint bump-version

PROJECT ?= driconfig
TESTS ?= tests

all:
	make clean
	make lint || exit 1
	make test || exit 1

clean:
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -f .coverage
	rm -rf htmlcov

check: format lint

format:
	uv run ruff format $(PROJECT) tests
	uv run ruff check --fix --unsafe-fixes $(PROJECT) $(TESTS)

--check-git-status:
	@status=$$(git status --porcelain); \
		if [ -n "$${status}" ]; \
		then \
			echo "ERROR:\n  GIT status is not clean.\
			\n  Commit or discard your changes before using this script."; \
			exit 1; \
		fi

lint:
	uv run ruff format --check $(PROJECT) $(TESTS)
	uv run ruff check $(PROJECT) $(TESTS)
	uv run mypy $(PROJECT)

lock:
	uv lock --no-update

test:
	uv run pytest --cov --cov-report=html --cov-report=xml

test-unit:
	uv run pytest --cov --cov-report=html --cov-report=xml -m "not integration"

test-integration:
	uv run pytest -m "integration"

test-files:
	diff --brief docs/index.md README.md

bump-version:
	@make -- --check-git-status
	@old_version=$$(uv version --dry-run --short); echo "Current version: $${old_version}"; \
		bmp_vrs=$(COMMIT_VERSION); \
		case $${bmp_vrs} in \
			major|minor|patch) echo "Version bumping: $${bmp_vrs}"; uv version --bump $${bmp_vrs}; ;; \
			*) echo "New version provided: $${bmp_vrs}"; uv version "$${bmp_vrs}"; ;; \
		esac; \
		new_version=$$(uv version --dry-run --short); \
		if [ "$${new_version}" = "$${old_version}" ]; then \
			echo "$${old_version} version update did not change the version number."; \
			exit 0; \
		else \
			uv sync; \
			uv run git commit pyproject.toml uv.lock -m ":bookmark: Bumping version from v$${old_version} to v$${new_version}"; \
			git tag -a "v$${new_version}" -m ":bookmark: Bumping version from v$${old_version} to v$${new_version}"; \
			echo "\nNew version: $${new_version}"; \
		fi

--setup-uv:
	@echo "Checking if uv is installed ..."; \
		uv_path=$$(command -v "uv"); \
		if [ -z "$${uv_path}" ]; \
		then \
			echo "ERROR: uv not found.\
			\n  You should have uv installed in order to setup this project.\
			\n  https://docs.astral.sh/uv/getting-started/installation/\n"; \
			exit 1; \
		fi
	@echo "Checking if uv.lock is up-to-date ..."; \
		if uv lock --check > /dev/null 2>&1 ; \
		then \
			echo "uv.lock is up-to-date"; \
            uv sync; \
  			uv run pre-commit install --install-hooks; \
		else \
  			echo "uv.lock is NOT up-to-date."; \
  			echo "Update uv.lock and commit it."; \
			uv sync; \
			uv run pre-commit install --install-hooks; \
			git add uv.lock; \
  			uv run pre-commit run --files uv.lock || true; \
  			uv run git commit .pre-commit-config.yaml uv.lock -m ":lock: Lock the project dependencies"; \
		fi

setup:
	@make -- --check-git-status || exit 1
	@make -- --setup-uv || exit 1
	@echo "Checking pre-commits ..."; poetry run pre-commit run --all-files || exit 1
	@echo "\nSetup completed successfully!\n"; exit 0
