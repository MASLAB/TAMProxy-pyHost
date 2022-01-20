from setuptools import setup

setup(
    name='tamproxy',
    version='0.1.1',

    description='TAMProxy Python Host',
    url='https://github.com/MASLAB/TAMProxy-pyHost',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.8',
    ],

    keywords='maslab tamproxy',
    packages=['tamproxy', 'tamproxy.comm', 'tamproxy.devices'],
    package_data={'tamproxy': ['config.yaml']},
    install_requires=['numpy>=1.13.3', 'pyserial>=3.0', 'PyYAML'],
)
