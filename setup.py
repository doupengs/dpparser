# coding: utf-8

from setuptools import setup
import dpparser


long_description = '''
     _                                      
  __| |_ __  _ __   __ _ _ __ ___  ___ _ __ 
 / _` | '_ \| '_ \ / _` | '__/ __|/ _ \ '__|
| (_| | |_) | |_) | (_| | |  \__ \  __/ |   
 \__,_| .__/| .__/ \__,_|_|  |___/\___|_|   
      |_|   |_| 
Analyze and clear web data.
If you are a crawler, this may be of interest to you.
'''

setup(
    name="dpparser",
    version=dpparser.__version__,
    author="doupeng",
    author_email="doupeng1993@sina.com",
    url="https://github.com/doupengs/dpparser",
    py_modules=['dpparser'],
    #packages=[''],
    description="The tools to parse the web page",
    long_description=long_description,
    license="Apache License 2.0",
    platforms=["Linux", "Windows"],
    install_requires=[
            'lxml',
            'dplog>=0.0.3',
        ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Intended Audience :: Developers",
        "License :: Apache License 2.0",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
