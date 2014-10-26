#!/usr/bin/env python

from setuptools import setup
from pip.req import parse_requirements
import os
import glob


def abspath(fname):
    return os.path.join(os.path.dirname(__file__), fname)

def read(fname, split=False):
    with open(abspath(fname)) as f:
        lines = f.read()
    if split:
        lines = lines.splitlines()
    return lines

def requirements(fname='requirements.txt'):
    return [str(r.req) for r in parse_requirements(abspath(fname))]

setup(name='biseq',
      version='0.0.1',
      description='Tools for analysing bisulfite sequencing data',
      author='Christof Angermueller',
      author_email='cangermueller@gmail.com',
      license='GNU GPLv3+',
      url='https://github.com/cangermueller/biseq',
      packages=['biseq'],
      scripts=glob.glob('scripts/*.py'),
      install_requires=requirements(),
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Education',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                   'Operating System :: MacOS',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.4',
                   ],
      keywords=['bisulfite sequencing', 'epigenetics']
      )
