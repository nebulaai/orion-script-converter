# setup.py

from setuptools import setup
setup(
    name='convert2orion',
    url='https://github.com/nebulaai/orion-script-converter',
    author='Eric Pang',
    packages=['converter'],
    version='0.0.1',
    license='MIT',
    description='An python package for converting Jupyter Notebook ".ipynb" files into python 3 ".py" files'
                ' and making a task file that can be run on Orion platform.',
    entry_points={
        'console_scripts': [
            'convert2py = converter.converter:convert2py',
            'convert2or = converter.converter:convert2or',
        ]
    },
    install_requires=[
        'pipreqs',
        'nbconvert',
    ]
)

