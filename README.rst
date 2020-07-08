================================
EMXlib plugin
================================

This plugin allows to import metadata to and from EMX format

Electron Microscopy eXchange (EMX) initiative was launched at the 2012 Instruct
Image Processing Center Developer Workshop with the intention of developing a
first set of standard conventions for the interchange of information for
single-particle analysis
(see `URL <http://heisenberg.cnb.csic.es:8080/emx/LoadHome.htm>`_
and `<https://www.ncbi.nlm.nih.gov/pubmed/26873784>`_ for details).


===================
Install this plugin
===================

You will need to use `3.0.0 <https://scipion-em.github.io/docs/release-3.0.0/docs/scipion-modes/how-to-install.html>`_ version of Scipion to run these protocols.

- **Stable version**

.. code-block::

      scipion installp -p scipion-em-emxlib

OR

  - through the plugin manager GUI by launching Scipion and following **Configuration** >> **Plugins**

- **Developer's version**

1. Download repository:

.. code-block::

            git clone https://github.com/scipion-em/scipion-em-emxlib.git

2. Install:

.. code-block::

            scipion installp -p path_to_scipion-em-emxlib --devel

- **Binary files**

No binary files are needed.

- **Tests**

To check the installation, simply run the following Scipion tests:

* scipion test emxlib.tests.test_workflow_emx.TestEmxWeb
* scipion test emxlib.tests.test_protocols_emx.TestEmxBase
* scipion test emxlib.tests.test_protocols_export_particles.TestExportParticlesEMX

=========
Protocols
=========

* emx export: export particles, micrograph, CTFs, etc to EMX format
* general import (particles, micrographs, etc) allow metadata information to be encoded using EMX conventions


========
Examples
========

See `URL <http://heisenberg.cnb.csic.es:8080/emx/LoadHome.htm>`_

===============
Buildbot status
===============

Status devel version:

.. image:: http://scipion-test.cnb.csic.es:9980/badges/emxlib_devel.svg

Status production version:

.. image:: http://scipion-test.cnb.csic.es:9980/badges/emxlib_prod.svg

