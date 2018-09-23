west_logs_analyzer
====================================================

command line utility to monitor error levels using ErrorGUI storage by comparing stacktraces Jaccard similarity
-------------------------------------------

.. image:: https://secure.travis-ci.org/imalkevich/west_logs_analyzer.png?branch=master
        :target: https://travis-ci.org/imalkevich/west_logs_analyzer

.. image:: https://codecov.io/github/imalkevich/west_logs_analyzer/coverage.svg?branch=master
    :target: https://codecov.io/github/imalkevich/west_logs_analyzer
    :alt: codecov.io

This utility is supposed to group different errors in groups based on stacktrace Jaccard similarity.

Installation
------------

::

    pip install west_logs_analyzer

or

::

    python setup.py install

Usage
-----

::

    usage: 
        1) From Anaconda Prompt cd to folder where README.rst is located
        2) Run the following commsnd: "python -m west_logs_analyzer.runner -u {database user} -p {database password} -i {days_interval}"

Author
------

-  Ihar Malkevich (imalkevich@gmail.com)