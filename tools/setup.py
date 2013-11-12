#!/usr/bin/env python
#from distribute_setup import use_setuptools
#use_setuptools()
from setuptools import setup
import sys

setup(name='coursera-tools',
      version='0.1',
      scripts=[
        'coursera_wget.sh',
        'coursera_parse.py',
       ],
     )
