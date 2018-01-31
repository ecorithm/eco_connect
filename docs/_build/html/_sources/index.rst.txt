Eco-Connect Documentation
=========================
Welcome to documentation for eco-connect, a thin python wrapper
for Ecorithm's API Platform.

Requirements
--------------------
* python >= 3.6

Installation
--------------------
eco-connect can be installed via pip from PyPI.

.. code-block:: shell

   pip install eco-connect

This will likely require the installation of a number of dependencies,
including Pandas, will require a compiler to compile required bits of code,
and can take a few minutes to complete.

All supported connectors require authentication via your provided
ecorithm username and password. These credentials are set through
environment variables and can be set by running the following commands
in shell:

.. code-block:: shell

   export ECO_CONNECT_USER="MY_ECORITHM_USERNAME"
   export ECO_CONNECT_PASSWORD="MY_ECORITHM_PASSWORD"

To verify your credentials and that the package has been installed correctly,
run the following in a pythoninterpreter of your choice:

.. code-block:: python

   from eco_connect import validate_credentials

   validate_credentials()

If everything was setup properly, you should see the print out:


*Ecorithm credentials successfully validated!*

Usage
------
All connectors can be imported directly from eco_connect.
For example, to import the FactsService connector:

.. code-block:: python

   from eco_connect import FactsService


Supported Connectors
--------------------

.. toctree::

    eco_connect.facts_service
