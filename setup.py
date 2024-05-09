# setup.py

from setuptools import setup, find_packages

setup(
    name='Stricture',
    version='1.0.8',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'stricture=stricture.cli:main'
        ]
    },
    install_requires=[
        'python-dateutil',
        'tzlocal',
        'argparse',
        'psutil',
        'pytz',
        'PyYAML',
        'freezegun'
    ],
    author='Jacob Moore',
    author_email='moorejacob2017@gmail.com',
    description='Stricture is a python package that provides classes and a CLI tool for easy scheduling, automating, and managing of specific operations.',
    long_description=open('description.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/moorejacob2017/Stricture/',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        #'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
    ],
    keywords='automation task job management date time cron schedule scheduling bash process pid command bash week month',
)