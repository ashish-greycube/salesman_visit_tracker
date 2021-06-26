# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in salesman_visit_tracker/__init__.py
from salesman_visit_tracker import __version__ as version

setup(
	name='salesman_visit_tracker',
	version=version,
	description='Sales CRM Customisations',
	author='Greycube',
	author_email='info@greycube.in',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
