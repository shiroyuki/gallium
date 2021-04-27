test-all:
	make test-one TEST_DIR=obj

test-one:
	./scripts/wrapper unittest discover -f -s gallium/$(TEST_DIR)

docs:
	source .venv/bin/activate && pip3 install -q pdoc3 && pdoc --force --html -o generated-docs gallium

docs-server: docs
	python3 -m http.server -d generated-docs/gallium 8080
