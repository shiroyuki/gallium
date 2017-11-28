PY=python3
PIP=pip3
G3_CLI=cd sample && gallium
LXC_IMAGE_TAG=shiroyuki/gallium
LXC_RUN_OPTS=
LXC_RUN_ARGS=

package: clean-dist
	@$(PY) setup.py sdist

install:
	@$(PIP) install -IU --force-reinstall dist/*

# Not using bdist_wheel due to permission issue.
clean-dist:
	@rm dist/* 2> /dev/null || echo '(/dist is clean...)'

release: clean-dist package
	@twine upload dist/*

# Build the test image.
docker-image:
	@docker build -t $(LXC_IMAGE_TAG) .

# Run the test image.
docker-run: docker-image
	@docker run -it --rm $(LXC_RUN_OPTS) $(LXC_IMAGE_TAG) $(LXC_RUN_ARGS)

test-unit:
	python3 -m unittest discover tests

# NOTE use for testing in isolation.
test-functional-isolation:
	@echo "[BEGIN] functional test in isolation"
	@make LXC_RUN_OPTS="--entrypoint=make" LXC_RUN_ARGS="test-functional" docker-image docker-run
	@echo "[ END ] functional test in isolation"

# NOTE use for testing locally.
test-functional: install-local
	@echo "-------------------------------------------------------------------------"
	@echo "RUN: WITHOUT THE SUBCOMMAND"
	@echo "========================================================================="
	@($(G3_CLI) || (echo "***** Exit with error code $$? *****"));
	@echo "-------------------------------------------------------------------------"
	@echo "RUN: THE FILE LISTER COMMAND"
	@echo "========================================================================="
	@($(G3_CLI) sample.file_lister ../ || (echo "***** Exit with error code $$? *****"));
	@echo "-------------------------------------------------------------------------"
	@echo "RUN: THE ARGS INSPECTOR (HELP)"
	@echo "========================================================================="
	@($(G3_CLI) --process-debug args.inspect -h || (echo "***** Exit with error code $$? *****"));
	@echo "-------------------------------------------------------------------------"
	@echo "RUN: THE ARGS INSPECTOR (EXECUTE)"
	@echo "========================================================================="
	@($(G3_CLI) --process-debug args.inspect || (echo "***** Exit with error code $$? *****"));
	@echo "-------------------------------------------------------------------------"
	@make uninstall-local

install-local:
	@$(PIP) install -qI --user .
	@make clean

uninstall-local:
	@$(PIP) uninstall -qy gallium

clean:
	@rm -rf build dist *.egg-info;
