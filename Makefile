package:
	@# For development only
	@python setup.py sdist

release:
	@python setup.py sdist upload # legacy
	@python setup.py sdist bdist_wheel upload
