# -*- coding: utf-8 -*-
##############################################################################
#
#  res-address, Simple Resource Address Parser
#  Copyright (C) 2018-2022 Mariano Ruiz
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


import unittest
from res_address import *


class TestAddresses(unittest.TestCase):

    def test_full_address(self):
        scheme, host, port, resource, query, username, password = get_res_address("localhost:27017/test")
        self.assertEqual(scheme, None)
        self.assertEqual(host, 'localhost')
        self.assertEqual(port, 27017)
        self.assertEqual(resource, "test")
        self.assertEqual(query, None)
        self.assertEqual(username, None)
        self.assertEqual(password, None)

    def test_localhost_and_resource(self):
        scheme, host, port, resource, query, username, password = get_res_address("localhost/test")
        self.assertEqual(scheme, None)
        self.assertEqual(host, 'localhost')
        self.assertIsNone(port)
        self.assertEqual(resource, "test")
        self.assertEqual(query, None)
        self.assertEqual(username, None)
        self.assertEqual(password, None)

    def test_query_string(self):
        scheme, host, port, resource, query, username, password = get_res_address("localhost/test?query=something&t=1")
        self.assertEqual(scheme, None)
        self.assertEqual(host, 'localhost')
        self.assertIsNone(port)
        self.assertEqual(resource, "test")
        self.assertEqual(query, "query=something&t=1")
        self.assertEqual(username, None)
        self.assertEqual(password, None)

    def test_remote_host_and_resource(self):
        scheme, host, port, resource, query, username, password = get_res_address("domain.com.ar/test")
        self.assertEqual(scheme, None)
        self.assertEqual(host, 'domain.com.ar')
        self.assertIsNone(port)
        self.assertEqual(resource, "test")
        self.assertEqual(query, None)
        self.assertEqual(username, None)
        self.assertEqual(password, None)

    def test_only_resource(self):
        scheme, host, port, resource, query, username, password = get_res_address("test")
        self.assertEqual(scheme, None)
        self.assertIsNone(host)
        self.assertIsNone(port)
        self.assertEqual(resource, 'test')
        self.assertEqual(query, None)
        self.assertEqual(username, None)
        self.assertEqual(password, None)

    def test_full_address_with_ip(self):
        scheme, host, port, resource, query, username, password = get_res_address("127.0.0.1:10001/test-prod")
        self.assertEqual(scheme, None)
        self.assertEqual(host, '127.0.0.1')
        self.assertEqual(port, 10001)
        self.assertEqual(resource, "test-prod")
        self.assertEqual(query, None)
        self.assertEqual(username, None)
        self.assertEqual(password, None)

    def test_port_and_resource(self):
        scheme, host, port, resource, query, username, password = get_res_address(":5000/test")
        self.assertEqual(scheme, None)
        self.assertIsNone(host)
        self.assertEqual(port, 5000)
        self.assertEqual(resource, "test")
        self.assertEqual(query, None)
        self.assertEqual(username, None)
        self.assertEqual(password, None)

    def test_ip_and_resource(self):
        scheme, host, port, resource, query, username, password = get_res_address("192.168.0.5/my_db")
        self.assertEqual(scheme, None)
        self.assertEqual(host, '192.168.0.5')
        self.assertIsNone(port)
        self.assertEqual(resource, "my_db")
        self.assertEqual(query, None)
        self.assertEqual(username, None)
        self.assertEqual(password, None)

    def test_scheme_ip_and_resource(self):
        scheme, host, port, resource, query, username, password = get_res_address("mongodb://192.168.0.5/my_db")
        self.assertEqual(scheme, "mongodb")
        self.assertEqual(host, '192.168.0.5')
        self.assertIsNone(port)
        self.assertEqual(resource, "my_db")
        self.assertEqual(query, None)
        self.assertEqual(username, None)
        self.assertEqual(password, None)

    def test_scheme_host_and_resource(self):
        scheme, host, port, resource, query, username, password = get_res_address("postgres://localhost/my_db")
        self.assertEqual(scheme, "postgres")
        self.assertEqual(host, 'localhost')
        self.assertIsNone(port)
        self.assertEqual(resource, "my_db")
        self.assertEqual(query, None)
        self.assertEqual(username, None)
        self.assertEqual(password, None)

    def test_ipv6_address(self):
        scheme, host, port, resource, query, username, password = get_res_address("[::10]/foo10")
        self.assertEqual(scheme, None)
        self.assertEqual(host, '[::10]')
        self.assertIsNone(port)
        self.assertEqual(resource, "foo10")
        self.assertEqual(query, None)
        scheme, host, port, resource, query, username, password = get_res_address("[2001:0db8:0000:0000:0000:ff00:0042:8329]/foo10")
        self.assertEqual(host, '[2001:0db8:0000:0000:0000:ff00:0042:8329]')
        self.assertIsNone(port)
        self.assertEqual(resource, "foo10")
        self.assertEqual(query, None)
        self.assertEqual(username, None)
        self.assertEqual(password, None)

    def test_scheme_ipv6_address(self):
        scheme, host, port, resource, query, username, password = get_res_address("ftp://[::10]/foo10")
        self.assertEqual(scheme, "ftp")
        self.assertEqual(host, '[::10]')
        self.assertIsNone(port)
        self.assertEqual(resource, "foo10")
        self.assertEqual(query, None)
        self.assertEqual(username, None)
        self.assertEqual(password, None)

    def test_ipv6_upper_case_address(self):
        scheme, host, port, resource, query, username, password = get_res_address("[2001:0DB8:0000:0000:0000:FF00:0042:8329]/TEST")
        self.assertEqual(scheme, None)
        self.assertEqual(host, '[2001:0DB8:0000:0000:0000:FF00:0042:8329]')
        self.assertIsNone(port)
        self.assertEqual(resource, "TEST")
        self.assertEqual(query, None)
        self.assertEqual(username, None)
        self.assertEqual(password, None)

    def test_ipv4_mapped_ipv6_address(self):
        scheme, host, port, resource, query, username, password = get_res_address("[::ffff:192.168.89.9]/test")
        self.assertEqual(scheme, None)
        self.assertEqual(host, '[::ffff:192.168.89.9]')
        self.assertIsNone(port)
        self.assertEqual(resource, "test")
        self.assertEqual(query, None)
        self.assertEqual(username, None)
        self.assertEqual(password, None)

    def test_ipv6_and_port_address(self):
        scheme, host, port, resource, query, username, password = get_res_address("[::1]:9999/foo")
        self.assertEqual(scheme, None)
        self.assertEqual(host, '[::1]')
        self.assertEqual(port, 9999)
        self.assertEqual(resource, "foo")
        self.assertEqual(query, None)
        self.assertEqual(username, None)
        self.assertEqual(password, None)

    def test_basic_auth(self):
        scheme, host, port, resource, query, username, password = get_res_address("user:pass@localhost:9999/foo")
        self.assertEqual(scheme, None)
        self.assertEqual(host, 'localhost')
        self.assertEqual(port, 9999)
        self.assertEqual(resource, "foo")
        self.assertEqual(query, None)
        self.assertEqual(username, "user")
        self.assertEqual(password, "pass")

    def test_basic_auth_ipv4(self):
        scheme, host, port, resource, query, username, password = get_res_address("user:pass@10.0.0.4/foo")
        self.assertEqual(scheme, None)
        self.assertEqual(host, '10.0.0.4')
        self.assertEqual(port, None)
        self.assertEqual(resource, "foo")
        self.assertEqual(query, None)
        self.assertEqual(username, "user")
        self.assertEqual(password, "pass")

    def test_basic_auth_ipv6(self):
        scheme, host, port, resource, query, username, password = get_res_address("user:pass@[::1]:2222/foo")
        self.assertEqual(scheme, None)
        self.assertEqual(host, '[::1]')
        self.assertEqual(port, 2222)
        self.assertEqual(resource, "foo")
        self.assertEqual(query, None)
        self.assertEqual(username, "user")
        self.assertEqual(password, "pass")

    def test_user_but_password(self):
        scheme, host, port, resource, query, username, password = get_res_address("user:@localhost:9999/foo")
        self.assertEqual(scheme, None)
        self.assertEqual(host, 'localhost')
        self.assertEqual(port, 9999)
        self.assertEqual(resource, "foo")
        self.assertEqual(query, None)
        self.assertEqual(username, "user")
        self.assertEqual(password, None)

    def test_user_but_password_and_without_separator(self):
        scheme, host, port, resource, query, username, password = get_res_address("user@localhost:9999/foo")
        self.assertEqual(scheme, None)
        self.assertEqual(host, 'localhost')
        self.assertEqual(port, 9999)
        self.assertEqual(resource, "foo")
        self.assertEqual(query, None)
        self.assertEqual(username, "user")
        self.assertEqual(password, None)

    def test_full_components(self):
        scheme, host, port, resource, query, username, password = get_res_address("mongodb+srv://user:pass@localhost:9999/foo")
        self.assertEqual(scheme, "mongodb+srv")
        self.assertEqual(host, 'localhost')
        self.assertEqual(port, 9999)
        self.assertEqual(resource, "foo")
        self.assertEqual(query, None)
        self.assertEqual(username, "user")
        self.assertEqual(password, "pass")

    def test_auth_with_noalpha_chars_components(self):
        scheme, host, port, resource, query, username, password = get_res_address("mongodb://a.b:p-.$%@localhost/test")
        self.assertEqual(scheme, "mongodb")
        self.assertEqual(host, 'localhost')
        self.assertEqual(port, None)
        self.assertEqual(resource, "test")
        self.assertEqual(query, None)
        self.assertEqual(username, "a.b")
        self.assertEqual(password, "p-.$%")


class TestWrongAddresses(unittest.TestCase):

    def test_invalid_port(self):
        self.assertRaises(InvalidPortError, get_res_address, "localhost:NotANumber/test")

    def test_empty_host(self):
        self.assertRaises(InvalidHostError, get_res_address, "/test")

    def test_invalid_host(self):
        self.assertRaises(InvalidHostError, get_res_address, "!/test")
        self.assertRaises(InvalidHostError, get_res_address, "!qwerty/test")
        self.assertRaises(InvalidHostError, get_res_address, "./test")
        self.assertRaises(InvalidHostError, get_res_address, "1000/test")

    def test_no_resource(self):
        self.assertRaises(NotResourceProvidedError, get_res_address, "test/")
        self.assertRaises(NotResourceProvidedError, get_res_address, "localhost:123/")
        self.assertRaises(NotResourceProvidedError, get_res_address, "http://host")
        self.assertRaises(NotResourceProvidedError, get_res_address, "http://host:1111")

    def test_missed_port(self):
        self.assertRaises(InvalidPortError, get_res_address, "127.1.1.10:/test")

    def test_invalid_ipv6_host(self):
        self.assertRaises(InvalidHostError, get_res_address, "[:::1/test")

    def test_invalid_chars_ipv6_host(self):
        self.assertRaises(InvalidHostError, get_res_address, "[:::1::xxx]/test")
        self.assertRaises(InvalidHostError, get_res_address, "[:::1:: ]:234/test")

    def test_port_with_invalid_chars(self):
        self.assertRaises(InvalidPortError, get_res_address, "localhost:a98/test")

    def test_port_with_spaces(self):
        self.assertRaises(InvalidPortError, get_res_address, "localhost: 98/test")

    def test_port_too_high_number(self):
        self.assertRaises(InvalidPortError, get_res_address, "localhost:70000/test")

    def test_resource_with_spaces(self):
        self.assertRaises(InvalidResourceError, get_res_address, "test/The Resource")
        self.assertRaises(InvalidResourceError, get_res_address, "localhost:123/ test")

    def test_invalid_resource(self):
        self.assertRaises(InvalidResourceError, get_res_address, "localhost:123/!name")
        self.assertRaises(InvalidResourceError, get_res_address, "$$")
        self.assertRaises(InvalidResourceError, get_res_address, "1234")

    def test_invalid_double_resource(self):
        self.assertRaises(AddressError, get_res_address, "localhost:123/name/secondname")

    def test_invalid_auth_resource(self):
        self.assertRaises(AddressError, get_res_address, "@localhost:123/db")
        self.assertRaises(AddressError, get_res_address, ":@localhost:123/db")
        self.assertRaises(AddressError, get_res_address, ":pass@localhost:123/db")
        self.assertRaises(AddressError, get_res_address, "user@pass@localhost:123/db")
