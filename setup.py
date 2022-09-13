# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from setuptools import setup


setup(
    name='pygments-ansi-color',
    version='0.0.6',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',
    install_requires=['pygments!=2.7.3'],
    packages=['pygments_ansi_color'],
    package_data={
        'pygments_ansi_color': ['py.typed'],
    },
    entry_points={
        'pygments.lexers': [
            'ansi_color = pygments_ansi_color:AnsiColorLexer',
        ],
    },
)
