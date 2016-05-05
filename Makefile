PY=python3
PIP=pip3
G3_CLI=cd sample && gallium
LXC_IMAGE_TAG=shiroyuki/gallium
LXC_RUN_OPTS=
LXC_RUN_ARGS=
package:
	@$(PY) setup.py sdist

# Not using bdist_wheel due to permission issue.
release:
	@$(PY) setup.py sdist upload

docker-image:
	docker build -t $(LXC_IMAGE_TAG) .

docker-run: docker-image
	docker run -it --rm $(LXC_RUN_OPTS) $(LXC_IMAGE_TAG) $(LXC_RUN_ARGS)

run-sample: install-local
	@echo "-------------------------------------------------------------------------"
	@echo "RUN: WITHOUT THE SUBCOMMAND"
	@echo "========================================================================="
	@($(G3_CLI) || (echo "Exit with error code $$?"));
	@echo "-------------------------------------------------------------------------"
	@echo "RUN: THE FILE LISTER COMMAND"
	@echo "========================================================================="
	@($(G3_CLI) sample.file_lister ../ || (echo "Exit with error code $$?"));
	@echo "-------------------------------------------------------------------------"
	@echo "RUN: THE ARGS INSPECTOR (HELP)"
	@echo "========================================================================="
	@($(G3_CLI) --process-debug args.inspect -h || (echo "Exit with error code $$?"));
	@echo "-------------------------------------------------------------------------"
	@echo "RUN: THE ARGS INSPECTOR (EXECUTE)"
	@echo "========================================================================="
	@($(G3_CLI) --process-debug args.inspect || (echo "Exit with error code $$?"));
	@echo "-------------------------------------------------------------------------"
	@make uninstall-local

install-local:
	@$(PIP) install -I --user .
	@make clean

uninstall-local:
	@$(PIP) uninstall -y gallium

clean:
	@rm -rf build dist *.egg-info;
