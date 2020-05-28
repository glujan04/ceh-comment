from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
import sys
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

version = '0.1.0'
setup(
	name='ceh-comment',
	version=version,
	description="plugin de comentarios para CKAN",
	long_description=long_description,
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='ckan, cehcomments, comments, commenting, discussion',
	author='Gary Lujan',
	author_email='glujan@idom.com',
	url='https://github.com/glujan04/ckanext-ceh-comment',
	license='AGPL',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
    [ckan.plugins]
	ceh_comment = ckanext.ceh_comment.plugin:CommentPlugin
	""",
)
