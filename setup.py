#!/usr/bin/env python

from setuptools import setup
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    
setup(
    name='plymouth-creator',
     python_requires='>3.5.2',
    version='1.3.1',
   author='Techcrafter',
      author_email='Techcrafter808@outlook.com',
    url='https://github.com/Techcrafter/Plymouth-Creator',
    description='A tool using GTK3 and Python to create your own plymouth boot animations',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=requirements,
    #packages=['plymouth-creator'],
)

