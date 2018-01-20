FactsService Documentation
=======================================
This connector is used to access the facts-service api via python.
For direct api documentation, please refer to
https://facts.prod.ecorithm.com/.

Example Usage
-------------

.. code-block:: python

   from eco_connect import FactsService

   facts_service = FactsService()

   facts_service.get_facts(building_id=26,
                           start_date='2017-12-20 00:00',
                           end_date='2017-12-21 00:00')

Supported Methods
-----------------
.. autoclass:: eco_connect.FactsService
  :members:
  :undoc-members:

Supported Formats
-----------------
* Pandas DataFrame
* List of Named tuples
* Csv
* Json (raw API response)
