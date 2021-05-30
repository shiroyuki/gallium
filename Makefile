.PHONY: test-all test-one docs-setup docs release

test-all:
	make test-one TEST_DIR=obj

test-one:
	./scripts/wrapper unittest discover -f -s gallium/$(TEST_DIR)

docs-setup:
	python -m venv .venv \
		&& bash -c "source .venv/bin/activate && pip3 install -r requirements-full.txt"

docs:
	bash -c "source .venv/bin/activate && python -m gallium.toolkit.docs build --full-build docs-src/source docs gallium"

release:
	python3 setup.py sdist
	twine upload dist/*
