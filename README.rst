Simple Resource Address Parser
==============================

Python module to parse simple network resource addresses, like the ones
used in many database systems to represent a database URI.

Used by `Mongotail <https://github.com/mrsarm/mongotail>`_
to parse the address passed through the command line, but can be used
by any other Python application that needs to parse a MongoDB database address,
or any other network resource like ``[SCHEMA://][[HOST OR IP][:PORT]/]RESOURCE``.

Usage:

.. code:: python

   >>> from res_address import get_res_address
   >>> schema, host, port, resource = get_res_address("localhost:27017/test")
   >>> print(schema, host, port, resource)
   None localhost 27017 test
   >>> schema, host, port, resource = get_res_address("my_db")
   >>> print(schema, host, port, resource)
   None None None my_db
   >>> schema, ipv6, port, resource = get_res_address("https://[::1]:9999/foo")
   >>> print(schema, ipv6, port, resource)
   https [::1] 9999 foo

The address can be:

+------------------------------+-----------------------------------------------------------------+
| foo                          | foo resource on local machine (IPv4 connection)                 |
+------------------------------+-----------------------------------------------------------------+
| 192.169.0.5/foo              | foo resource on 192.168.0.5 machine                             |
+------------------------------+-----------------------------------------------------------------+
| remotehost/foo               | foo resource on *remotehost* machine                            |
+------------------------------+-----------------------------------------------------------------+
| 192.169.0.5:9999/foo         | foo resource on 192.168.0.5 machine on port 9999                |
+------------------------------+-----------------------------------------------------------------+
| http://192.169.0.5:9999/foo  |  foo resource on 192.168.0.5 machine on port 9999, schema http  |
+------------------------------+-----------------------------------------------------------------+
| "[::1]:9999/foo"             | foo resource on ::1 machine on port 9999 (IPv6 connection)      |
+----------------------+-------------------------------------------------------------------------+
| :1234/foo                    | foo resource on port 1234                                       |
+----------------------+-------------------------------------------------------------------------+

Some validations are performed over the host, port and resource strings, and an
exception is launched if some of the checks fail, but take into account that
invalid range of IP addresses or incompatible resource names may pass:

.. code:: python

   >>> host, port, resource = get_res_address("localhost:INVALIDport/test")
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "res_address/__init__.py", line 74, in get_res_address
       raise InvalidPortError('Invalid port number "%s"' % port, address, port)
   res_address.InvalidPortError: Invalid port number "INVALIDport"

All the validation exceptions inherit from ``AddressError``:

* ``InvalidHostError``
* ``InvalidPortError``
* ``InvalidResourceError``
* ``NotResourceProvidedError``

Query strings passed in the address are ignored. User and password in the
URL are not supported yet, an ``InvalidHostError`` is raised if it's the case.

Run the test
------------

Just execute (Python 2.7 or 3.5+)::

   $ python setup.py test


Or::

   $ python -m unittest -v tests


About
-----

Project: https://github.com/mrsarm/python-res-address

Authors: (2018-2022) Mariano Ruiz <mrsarm@gmail.cm>

License: LGPL-3
