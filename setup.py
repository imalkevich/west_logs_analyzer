from setuptools import setup, find_packages
import west_logs_analyzer
import os

def extra_dependencies():
    import sys
    ret = []
    if sys.version_info < (3, 6):
        ret.append('argparse')
    return ret


def read(*names):
    values = dict()
    extensions = ['.txt', '.rst']
    for name in names:
        value = ''
        for extension in extensions:
            filename = name + extension
            if os.path.isfile(filename):
                value = open(name + extension).read()
                break
        values[name] = value
    return values

long_description = """
%(README)s

News
====

%(CHANGES)s

""" % read('README', 'CHANGES')

setup(
    name='west_logs_analyzer',
    version=west_logs_analyzer.__version__,
    description='command line utility to monitor error levels using ErrorGUI storage by comparing stacktraces Jaccard similarity',
    long_description=long_description,
    classifiers=[
        "Development Status :: 1 - Development",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Documentation",
    ],
    keywords='west logs analyzer',
    author='Ihar Malkevich',
    author_email='imalkevich@gmail.com',
    maintainer='Ihar Malkevich',
    maintainer_email='imalkevich@gmail.com',
    url='https://github.com/imalkevich/west_logs_analyzer',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'west_logs_analyzer = west_logs_analyzer.west_logs_analyzer:command_line_runner',
        ]
    },
    install_requires=[
        'cx_Oracle',
        'datasketch',
        'PTable'
    ] + extra_dependencies(),
    #test_require = ['coverage', 'codecov']
)