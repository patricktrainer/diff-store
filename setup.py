
from setuptools import setup, find_packages

setup(
    name='diff_store',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'gitpython',
    ],
    entry_points={
        'console_scripts': [
            'diff_store = diffstore.script:main',
        ],
    },
)
