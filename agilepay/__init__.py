# -*- coding: utf-8 -*-

#     ___         _ __     ____
#    /   | ____ _(_/ ___  / __ \____ ___  __
#   / /| |/ __ `/ / / _ \/ /_/ / __ `/ / / /
#  / ___ / /_/ / / /  __/ ____/ /_/ / /_/ /
# /_/  |_\__, /_/_/\___/_/    \__,_/\__, /
#       /____/                     /____/

"""
AgilePay python sdk
~~~~~~~~~~~~~~~~~~~

This is the official agilepay python sdk

Basic usage :

>>> from agilepay import AgilePay
>>> ap = AgilePay({'api_key': '...', 'api_secret': '...'})

--- create a gateway:

>>> gateway = ap.gateway().create('stripe', {'secret_key': '...'})

--- create a payment method

>>> card = ap.payment_method().create_card(gateway, {
... 'cvv': '',
... 'number': '',
... 'holder_name': '',
... 'expiry_year': '',
... 'expiry_month': '',
... })

--- great! now let's charge 5 pounds

>>> ap.transaction()
...    .set_payment_method(card)
...    .set_gateway(gateway)
...    .auth('500', 'gbp')

"""

from agilepay import AgilePay
