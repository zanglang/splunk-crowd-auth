from setuptools import setup

dependencies = ['Crowd']

setup(
    name='splunk-crowd-auth',
    url='https://github.com/Dwolla/splunk-crowd-auth.git',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'splunk-crowd-auth = crowd_scripted:main'
        ]
    },

    classifiers=[
        'Environment :: Console',
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration :: Authentication/Directory"
    ]
)
