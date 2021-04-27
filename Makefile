.PHONY: test-all test-one docs docs-server release

test-all:
	make test-one TEST_DIR=obj

test-one:
	./scripts/wrapper unittest discover -f -s gallium/$(TEST_DIR)

docs:
	source .venv/bin/activate && pip3 install -q pdoc3 && pdoc --force --html -o generated-docs gallium
	cp -rv generated-docs/gallium/* docs

docs-server: docs
	python3 -m http.server -d docs 8080

release:
	python3 setup.py sdist
	twine upload dist/*
