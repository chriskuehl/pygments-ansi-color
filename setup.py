# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from setuptools import setup


setup(
    name='pygments-ansi-color',
    version='0.0.2',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=['pygments'],
    py_modules=['pygments_ansi_color'],
    entry_points={
        'pygments.lexers': [
            'ansi_color = pygments_ansi_color:AnsiColorLexer',
        ],
    },
)
