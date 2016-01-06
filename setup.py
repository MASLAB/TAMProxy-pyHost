from setuptools import setup

setup(
    name='tamproxy',
    version='0.0.2',

    description='TAMProxy Python Host',
    url='https://github.com/mitchgu/TAMProxy-pyHost',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='maslab tamproxy',
    packages=['tamproxy'],
    install_requires=['numpy', 'pyserial>=3.0', 'PyYAML'],
)
