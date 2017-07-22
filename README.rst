About
=====

This is a Python wrapper library for the `ShipStation API <http://docs.shipstation.apiary.io>`_.

It supports retrieving paged lists of resources based on filters. Create/update is not yet supported but would be trivial to add.

All models/resources referenced in the ShipStation API developer docs are wrapped (orders, shipments, products, etc.).

Usage
=====

.. code:: python

    from shipstation import ShipStationApi

    svc = ShipStationApi(
          api_key='your_api_key',
          api_secret='your_api_secret'
    )

    shipped_filter = {'orderStatus': 'shipped'}
    print "You have %s shipped orders" % svc.shipments.count(shipped_filter)

    pages = svc.shipments.page_count(shipped_filter)
    for p in xrange(pages):
          shipments = svc.shipments.page(shipped_filter, page_num=p+1)
          for each s in shipments:
              do_something_with_the_shipment_i_guess(s)


    order = svc.orders.page({'orderNumber':'AN-ORDER-NUMBER'})
    print order[0]  # note that all response are iterable, even if there is only 1

::


TODOs
=====

1. Add tests
2. Add CI
3. Release on PyPI
4. Add create/update (for endpoints that support it)
