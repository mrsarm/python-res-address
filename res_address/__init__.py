# -*- coding: utf-8 -*-
##############################################################################
#
#  res-address, Simple Resource Address Parser
#  Copyright (C) 2018i Mariano Ruiz (<https://github.com/mrsarm/python-res-address>).
#
#  Author: Mariano Ruiz <mrsarm@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this programe.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


__author__ = 'Mariano Ruiz'
__version__ = '1.0.0-b1'
__license__ = 'LGPL-3'
__url__ = 'https://github.com/mrsarm/python-res-address'
__doc__ = """Simple Resource Address Parser."""


def get_res_address(address):
    """
    :param address: the address, possible values are:
        foo                   foo database on local machine (IPv4 connection)
        192.169.0.5/foo       foo database on 192.168.0.5 machine
        192.169.0.5:9999/foo  foo database on 192.168.0.5 machine on port 9999
        "[::1]:9999/foo"      foo database on ::1 machine on port 9999 (IPv6 connection)
    :return: a tuple with ``(host, port, db name)``. If one or more value aren't in the `address`
    string, ``None`` is set in the tuple value
    """
    host = port = dbname = None
    if '/' in address:
        if address.startswith("/"):
            raise InvalidHostError('Missed host at "%s"' % address)
        if address.endswith("/"):
            raise NotDatabaseProvidedError('Missed dbname at "%s"' % address)
        host, dbname = address.split('/')
        if host.startswith("[") and "]" in host:
            # IPv6 address
            # See http://api.mongodb.org/python/2.8/api/pymongo/connection.html
            # If the connection is refused, you have to ensure that `mongod`
            # is running with `--ipv6` option enabled, and "bind_ip" value are
            # disabled in `mongod.conf`, or is enabled with your
            # IPv6 address in the list.
            if "]:" in host:
                port = host[host.index("]:")+2:]
                host = host[:host.index("]:")+1]
        elif ':' in host:
            # IPv4 address
            try:
                host, port = host.split(':')
            except ValueError:
                raise InvalidHostError('Invalid host "%s"' % host)
        if port is not None:
            try:
                port = int(port)
            except ValueError:
                raise InvalidPortError('Invalid port number "%s"' % port)
    else:
        if (address.startswith("[") and address.rfind("]") > address.rfind(":")) \
                or ":" in address or "." in address:
            raise NotDatabaseProvidedError('No database name provided in "%s"' % address)
        dbname = address
    if host == '':
        host = None
    return host, port, dbname


#
# Exceptions declaration
#

class AddressError(ValueError):
    def __init__(self, message):
        self.message = message


class InvalidHostError(AddressError):
    def __init__(self, message):
        super(InvalidHostError, self).__init__(message)


class InvalidPortError(AddressError):
    def __init__(self, message):
        super(InvalidPortError, self).__init__(message)


class NotDatabaseProvidedError(AddressError):
    def __init__(self, message):
        super(NotDatabaseProvidedError, self).__init__(message)
