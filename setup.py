# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 22:03:55 2024

@author: Hogan
"""

from setuptools import setup

setup(
	name='tongubako',
	version='0.1.1',
	description='Hogan Tong\'s tool box',
	url='https://github.com/HoagieTung/tongubako',
	author='Hogan Tong',
	author_email='homo.ignotus@outlook.com',
	license='unlicense',
	packages=['tongubako'],
	install_requires=[
		'pdblp',
		'pandas',
		'numpy',
		'bs4',
		'sqlalchemy',
		'pymsteams'],
	zip_safe=False
)