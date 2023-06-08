from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in rashidbrothers/__init__.py
from rashidbrothers import __version__ as version

setup(
	name="rashidbrothers",
	version=version,
	description="this is bussiness erp application",
	author="Tech Ventures",
	author_email="safdar211@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
