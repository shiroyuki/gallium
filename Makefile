package:
	@python3 setup.py sdist

# Not using bdist_wheel due to permission issue.
release:
	@python3 setup.py sdist upload
