from setuptools import setup

dependencies = ['python-crowd']

setup(
    name='splunk-crowd-auth',
    url='https://github.com/Dwolla/splunk-crowd-auth.git',
    install_requires=dependencies,

    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration :: Authentication/Directory"
    ]
)
