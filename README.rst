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
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
.. |docs| image:: https://readthedocs.org/projects/python-reverse_communication_iterative_solver/badge/?style=flat
    :target: https://python-reverse_communication_iterative_solver.readthedocs.io/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/enricofacca/python-reverse_communication_iterative_solver/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/enricofacca/python-reverse_communication_iterative_solver/actions

.. |requires| image:: https://requires.io/github/enricofacca/python-reverse_communication_iterative_solver/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/enricofacca/python-reverse_communication_iterative_solver/requirements/?branch=master

.. |wheel| image:: https://img.shields.io/pypi/wheel/reverse-communication-iterative-solver.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/reverse-communication-iterative-solver

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/reverse-communication-iterative-solver.svg
    :alt: Supported versions
    :target: https://pypi.org/project/reverse-communication-iterative-solver

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/reverse-communication-iterative-solver.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/reverse-communication-iterative-solver



.. end-badges

This package aims to provide a common template for building iterative solvers, 
those solver that approximate problem solutions with incremental steps (called "update" in this project).
This template will over a minimal base for developing, tuning and using iterative solvers from the earliest 
protypting phase to the delivery of block box algorithm.

The interface between an (advanced) user and the iterative solver is decomposed into the following 4 main phases

1. set the solver controls and problem inputs before the next update;
2. reset the solver controls reset problem inputs after a update failure; 
3. study any you want combaning the information from problem, unknows, and solver;
4. set when the solver has finished its job.

This decomposition is done via a Reverse Communication (RC) 
approach, an old style of programming used for 
example in the `ARPACK <https://www.caam.rice.edu/software/ARPACK/>`_ library, combined with Python classes. 
We adopt this approach because it let the user work "manually" on the structures
describing its problem instead of having to define in advance 
the procedure to handle the steps 1,2,3,4. This is particularly convient in early step of
the algorithm development. A nicer and clenear function hiding the RC cycle to an user who 
wants a block-box solver can be easily build.


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
