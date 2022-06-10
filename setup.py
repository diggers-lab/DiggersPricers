from setuptools import find_packages, setup
setup(
    name='OpenFinPriGen',
    packages=find_packages(include=['OpenFinPriGen']),
    version='0.1.0',
    description='Diggers Project Library',
    author='Zachary Scialom',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
