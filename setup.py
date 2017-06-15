import os
from distutils.core import Command
from setuptools import setup, find_packages

__here__ = os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":
    name = 'demo_rules'

    setup(
        name=name,
        version='1.0',
        description="Demonstration Insights Rules",
        keywords='insights-rules',
        packages=find_packages(),
        install_requires=[
            'insights-core',
        ],
        extras_require={'develop': [
            'coverage',
            'pytest',
            'pytest-cov',
        ], 'optional': [
            'python-cjson'
        ]
        },
        cmdclass={
        }
    )
