package:
	@python3 setup.py sdist

# Not using bdist_wheel due to permission issue.
release:
	@python3 setup.py sdist upload

run-sample: install-local
	bin/run_sample
	make uninstall-local

install-local:
	pip install -I --user .
	make clean

uninstall-local:
	pip uninstall -y gallium

clean:
	rm -rf build dist *.egg-info;
