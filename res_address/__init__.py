# -*- coding: utf-8 -*-
##############################################################################
#
#  res-address, Simple Resource Address Parser
#  Copyright (C) 2018-2019 Mariano Ruiz
#  https://github.com/mrsarm/python-res-address
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
#  along with this library.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


__author__ = 'Mariano Ruiz'
__version__ = '1.0.0-b2'
__license__ = 'LGPL-3'
__url__ = 'https://github.com/mrsarm/python-res-address'
__doc__ = """Simple Resource Address Parser."""


import re


def get_res_address(address):
    """
    :param address: the address, possible values are:
        foo                   foo resource on local machine (IPv4 connection)
        192.169.0.5/foo       foo resource on 192.168.0.5 machine
        192.169.0.5:9999/foo  foo resource on 192.168.0.5 machine on port 9999
        "[::1]:9999/foo"      foo resource on ::1 machine on port 9999 (IPv6 connection)
    :return: a tuple with ``(host, port, db name)``. If one or more value aren't in the `address`
    string, ``None`` is set in the tuple value
    """
    host = port = resource = None
    is_ipv6 = False
    if '/' in address:
        if address.startswith("/"):
            raise InvalidHostError('Missed host at "%s"' % address, address)
        if address.endswith("/"):
            raise NotResourceProvidedError('Missed resource at "%s"' % address, address)
        host, resource = address.split('/')
        if host.startswith("[") and "]" in host:
            is_ipv6 = True
            # IPv6 address
            if "]:" in host:
                port = host[host.index("]:")+2:]
                host = host[:host.index("]:")+1]
            if not re.compile(r'^\[[\d:a-h]+\]').search(host):
                raise InvalidHostError('Invalid host "%s"' % host, address, host)
        elif ':' in host:
            # IPv4 address
            try:
                host, port = host.split(':')
            except ValueError:
                raise InvalidHostError('Invalid host "%s"' % host, address, host)
        if port is not None:
            if re.compile(r'^\d{1,5}$').search(port):
                port = int(port)
                if port > 65535:
                    raise InvalidPortError('Too high port number "%s"' % port, address, port)
            else:
                raise InvalidPortError('Invalid port number "%s"' % port, address, port)
    else:
        if (address.startswith("[") and address.rfind("]") > address.rfind(":")) \
                or ":" in address or "." in address:
            raise NotResourceProvidedError('No resource name provided in "%s"' % address, address)
        resource = address
    if host == '':
        host = None
    elif host and not is_ipv6 and not re.compile(r'^[\w\-_.]+$').search(host):
        raise InvalidHostError('Invalid host "%s"' % host, address, host)
    if not re.compile(r'^[\w\-_]+$').search(resource):
        raise InvalidResourceError('Invalid resource "%s"' % resource, address, resource)
    return host, port, resource


#
# Exceptions declaration
#

class AddressError(ValueError):
    def __init__(self, message, address=None, invalid_component=None):
        self.message = message
        self.address = address
        self.invalid_component = invalid_component

    def __str__(self):
        return self.message


class InvalidHostError(AddressError):
    pass


class InvalidPortError(AddressError):
    pass


class InvalidResourceError(AddressError):
    pass


class NotResourceProvidedError(AddressError):
    pass
