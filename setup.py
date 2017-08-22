from setuptools import setup

setup(
    name='hello',
    version='0.1',
    py_modules=['hello'],
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        hello=hello:cli
    ''',
)
