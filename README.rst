AgilePay Python SDK
===================

The AgilePay Python sdk will provide convenient access to the AgilePay
API from applications written in the Python language. It will include a
pre-defined set of classes for API resources that initialize themselves
dynamically from API responses which makes it compatible with a wide
range of versions of the AgilePay API.

Documentation
-------------

See the `Python API docs`_.

Installation
------------

::

    pip install --upgrade agilepay

or

::

    easy_install --upgrade agilepay

Install from source with:

::

    python setup.py install

Usage
-----

Register for an account and get your api\_key and secret at `AgilePay`_.

.. code:: python

    import agilepay

    agile_pay = AgilePay({
        'api_key': 'key',
        'api_secret': 'secret'
    })

Gateways
--------

To create a new gateway :
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    gateway = agile_pay.gateway().create('stripe', {'secret_key': 'stripe-secret-key'})

The response body will contain a gateway **reference** which is used to
perform transactions against the gateway

.. code:: python

    gateway_reference = gateway.get_body()['reference']

Payment methods
---------------

To create a new payment method type of gateway token:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this case the payment method will be retained with the provided
gateway, please check the availability of transaction store in the
gateways list

Gateways list -> http://docs.agilepay.io/#!/gateway

Gateway token ->
http://docs.agilepay.io/#!/payment-method-create-gateway-token

.. code:: python

    payment_method = agile_pay.payment_method().create_gateway_token(gateway_reference, {
        'cvv': '123',
        'number': '4111111111111111',
        'holder_name': 'Mario Rossi',
        'expiry_month': '12',
        'expiry_year': '17'
    })

The response body will contain a payment method **token** which is used
to perform transactions against the payment method

.. code:: python

    payment_method_token = payment_method.get_body()['token']

Transactions
------------

Auth (Charge a credit card with a payment method type of gateway token):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    transaction = agile_pay.transaction().set_payment_method(payment_method_gateway_token).auth(5000, 'EUR') # charging 5.00 euros

The response will contain a **reference** which can be used for second
steps transactions such as **void**, **capture** and **credit**

.. code:: python

     transaction_reference = transaction.get_body()['reference']

Void (Cancel an authorized transaction):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    response = agile_pay.transaction(transaction_reference).void();

Capture (Settle an authorized transaction):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    response = agile_pay.transaction(transaction_reference).capture();

Credit (Refund a settled transaction):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    response = agile_pay.transaction(transaction_reference).credit();

Response methods
~~~~~~~~~~~~~~~~

Below the response object available methods.

.. code:: python

    get_status_code() # Retrieves the response status code

.. code:: python

    get_body() # retrieves the response body as a dictionary

.. _Python API docs: http://docs.agilepay.io/#!/introduction
.. _AgilePay: support@agilepay.io