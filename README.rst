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
   >>> scheme, host, port, resource, query, username, password = get_res_address("localhost:27017/test?timeout=5")
   >>> print(scheme, host, port, resource, query, username, password)
   None localhost 27017 test timeout=5 None None
   >>> print(get_res_address("my_db"))
   (None, None, None, 'my_db', None, None, None)
   >>> scheme, ipv6, port, resource, query, username, password = get_res_address("https://[::1]:9999/foo")
   >>> print(scheme, ipv6, port, resource)
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
| http://192.169.0.5:9999/foo  | foo resource on 192.168.0.5 machine on port 9999, scheme http   |
+------------------------------+-----------------------------------------------------------------+
| "[::1]:9999/foo"             | foo resource on ::1 machine on port 9999 (IPv6 connection)      |
+----------------------+-------------------------------------------------------------------------+
| :1234/foo                    | foo resource on port 1234                                       |
+------------------------------+-----------------------------------------------------------------+
| user:pass@localhost/foo      | foo resource on localhost, with basic authentication            |
+------------------------------+-----------------------------------------------------------------+
| localhost/foo?timeout=500    | foo resource on localhost, with query string                    |
+----------------------+-------------------------------------------------------------------------+

**The only required component in the URI is the resource**. Some validations are performed over the
host, port and resource strings, and an exception is launched if some of the checks fail, but take
into account that invalid range of IP addresses or incompatible resource names may pass:

.. code:: python

   >>> address = get_res_address("localhost:INVALIDport/test")
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


Difference with urllib.parse
----------------------------

If you need a library that can fully parse web URLs you should use
`urllib.parse <https://docs.python.org/3/library/urllib.parse.html>`_ instead. This
library intends to be used with simpler URIs for database resources, with only one
resource name set, e.g. "my_db" or "localhost:123/my_db", but not "localhost:123/my_db/my_table".
Also a URL like "localhost:123" that is a valid HTTP URL, is not as
database URL because the "resource" (the database name) is not set.

Also to get the keys and values of the query component returned by ``get_res_address()``,
a function like ``urllib.parse.parse_qs()`` is recommended::

.. code:: python

   >>> from res_address import get_res_address
   >>> from urllib.parse import parse_qs
   >>> scheme, host, port, resource, query, username, password = get_res_address("localhost/db?timeout=500")
   >>> parse_qs(query).get('timeout', None)
   ['500']


Run the tests
-------------

Just execute (Python 2.7 or 3.5+)::

   $ python setup.py test


Or::

   $ python -m unittest -v tests


About
-----

Project: https://github.com/mrsarm/python-res-address

Authors: (2018-2022) Mariano Ruiz <mrsarm@gmail.cm>

License: LGPL-3
