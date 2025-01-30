from __future__ import annotations

from setuptools import setup


setup(
    name='pygments-ansi-color',
    version='0.3.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.9',
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
