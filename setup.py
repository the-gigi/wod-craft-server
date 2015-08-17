from setuptools import setup, find_packages

setup(
    name='wodcraft_api',
    version='0.1',
    license='LICENSE',
    author='Gigi Sayfan',
    author_email='the.gigi@gmail.com',
    url='https://github.com/wod-craft/wodcraft/api',
    description='RESET API for collecting personal records',
    long_description=open('README.md').read(),
    packages=find_packages(exclude=['tests']),
    namespace_packages=['wodcraft'],
    scripts=[],
    setup_requires=['nose>=1.3.7', 'coverage>=3.7.1'],
    test_suite='nose.collector',
    entry_points = {
        'console_scripts': [
            'run = aclima.backend_api_server.run:run'
        ]
    },
)
