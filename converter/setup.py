# setup.py

from setuptools import setup
setup(
    name='converter2py',
    url='https://github.com/jladan/package_demo',
    author='Eric Pang',
    packages=['converter'],
    version='0.0.1',
    license='MIT',
    description='An python package for converting Jupyter Notebook .ipynb files into python 3 .py files'
                ' and making a task file that can be run on Orion platform.',
    entry_points={
        'console_scripts': [
            'convert2py = converter.converter:main',
        ]
    },
    install_requires=[
        'pipreqs',
        'nbconvert',
    ]
)
