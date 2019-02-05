Simple Resource Address Parser
==============================

Work in progress, not published yet ...

Python module to parse simple network resource addresses, like the ones
used in many database systems to represent a database URI.

``res_address`` will be used by `Mongotail <https://github.com/mrsarm/mongotail>`_
to parse the address passed through command line (migration in progress), but can be used
by any other Python application that needs to parse a MongoDB database address,
or any other network resource like ``[[HOST OR IP][:PORT]/]RESOURCE``.

Usage::

   >>> from res_address import get_res_address
   >>> host, port, resource = get_res_address("localhost:27017/test")
   >>> print(host, port, resource)
   localhost 27017 test
   >>> host, port, resource = get_res_address("my_db")
   >>> print(host, port, resource)
   None None my_db
   >>> ipv6, port, resource = get_res_address("[::1]:9999/foo")
   >>> print(ipv6, port, resource)
   [::1] 9999 foo



The address can be:

+----------------------+-------------------------------------------------------------+
| foo                  | foo resource on local machine (IPv4 connection)             |
+----------------------+-------------------------------------------------------------+
| 192.169.0.5/foo      | foo resource on 192.168.0.5 machine                         |
+----------------------+-------------------------------------------------------------+
| remotehost/foo       | foo resource on *remotehost* machine                        |
+----------------------+-------------------------------------------------------------+
| 192.169.0.5:9999/foo | foo resource on 192.168.0.5 machine on port 9999            |
+----------------------+-------------------------------------------------------------+
| "[::1]:9999/foo"     | foo resource on ::1 machine on port 9999 (IPv6 connection)  |
+----------------------+-------------------------------------------------------------+
| :1234/foo            | foo resource on port 1234                                   |
+----------------------+-------------------------------------------------------------+

Some validations over the host, port and resource strings are performed, and an
exception is launched if some of the checks fails, but take into account that
invalid range IPs or incompatible resource names may pass.::

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


Run the test
------------

Just execute (Python 2 or 3)::

   $ python setup.py test


Or::

   $ python -m unittest -v tests


About
-----

Project: https://github.com/mrsarm/python-res-address

Authors: (2018-2019) Mariano Ruiz <mrsarm@gmail.cm>

License: LGPL-3
