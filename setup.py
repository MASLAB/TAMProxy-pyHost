from setuptools import setup

setup(
    name='tamproxy',
    version='0.0.6',

    description='TAMProxy Python Host',
    url='https://github.com/mitchgu/TAMProxy-pyHost',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='maslab tamproxy',
    packages=['tamproxy', 'tamproxy.comm', 'tamproxy.devices'],
    package_data={'tamproxy': ['config.yaml']},
    install_requires=['numpy', 'pyserial>=3.0', 'PyYAML'],
)
