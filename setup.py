#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='passer',
      version='0.1',
      description='46elks and Twitter connector',
      url='https://github.com/46elks/passer',
      author='Emil Tullstedt'
      author_email='emil@46elks.com',
      license='MIT',
      packages=find_packages(),
      packages_dir = {'': 'passer'}
     )
