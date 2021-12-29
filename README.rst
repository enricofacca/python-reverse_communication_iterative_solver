========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |github-actions| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-reverse_communication_iterative_solver/badge/?style=flat
    :target: https://python-reverse_communication_iterative_solver.readthedocs.io/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/enricofacca/python-reverse_communication_iterative_solver/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/enricofacca/python-reverse_communication_iterative_solver/actions

.. |requires| image:: https://requires.io/github/enricofacca/python-reverse_communication_iterative_solver/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/enricofacca/python-reverse_communication_iterative_solver/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/enricofacca/python-reverse_communication_iterative_solver/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/enricofacca/python-reverse_communication_iterative_solver

.. |version| image:: https://img.shields.io/pypi/v/reverse-communication-iterative-solver.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/reverse-communication-iterative-solver

.. |wheel| image:: https://img.shields.io/pypi/wheel/reverse-communication-iterative-solver.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/reverse-communication-iterative-solver

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/reverse-communication-iterative-solver.svg
    :alt: Supported versions
    :target: https://pypi.org/project/reverse-communication-iterative-solver

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/reverse-communication-iterative-solver.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/reverse-communication-iterative-solver

.. |commits-since| image:: https://img.shields.io/github/commits-since/enricofacca/python-reverse_communication_iterative_solver/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/enricofacca/python-reverse_communication_iterative_solver/compare/v0.0.0...master



.. end-badges

Python package/template to build iterative solver via reverse communication and classes

* Free software: GNU Lesser General Public License v3 or later (LGPLv3+)

Installation
============

::

    pip install reverse-communication-iterative-solver

You can also install the in-development version with::

    pip install https://github.com/enricofacca/python-reverse_communication_iterative_solver/archive/master.zip


Documentation
=============


https://python-reverse_communication_iterative_solver.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
