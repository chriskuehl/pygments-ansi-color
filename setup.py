from __future__ import annotations

from pathlib import Path

from setuptools import setup


long_description = (Path(__file__).parent / 'README.md').read_text()


setup(
    name='pygments-ansi-color',
    version='0.3.0',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Other',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: System :: Shells',
        'Topic :: Terminals',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
    python_requires='>=3.10',
    install_requires=['pygments!=2.7.3'],
    packages=['pygments_ansi_color'],
    package_data={
        'pygments_ansi_color': ['py.typed'],
    },
    entry_points={
        'pygments.lexers': [
            'ansi-color = pygments_ansi_color:AnsiColorLexer',
        ],
        'pygments.formatters': [
            'ansi-html = pygments_ansi_color:AnsiHtmlFormatter',
        ],
    },
)
