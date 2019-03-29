# setup.py

from setuptools import setup
setup(
    name='convert2orion',
    url='https://github.com/nebulaai/orion-script-converter',
    author='Eric Pang',
    packages=['converter'],
    version='0.0.1',
    license='MIT',
    description='Warp and convert python3 project files into a NBAI task '
                'that can be uploaded directly via NBAI Orion Platform and executed by Nebula AI Worker.',
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

