Facts-Service
=======================================
This connector is used to access the facts-service api via python.
For direct api documentation, please refer to
https://facts.prod.ecorithm.com/api/v1/doc.

Example Usage
-------------

.. code-block:: python

   from eco_connect import FactsService

   facts_service = FactsService()

   data = facts_service.get_facts(building_id=26,
                                  start_date='2017-12-20 00:00',
                                  end_date='2017-12-21 00:00',
                                  result_format='pandas')


FactsService
------------
.. autoclass:: eco_connect.FactsService


.. toctree::
   facts_service.get_facts
   facts_service.put_facts
   facts_service.get_point_mapping
   facts_service.get_native_names
   facts_service.get_equipment
