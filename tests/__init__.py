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
        expected = (None, 'localhost', 27017, "test", None, None, None)
        result = get_res_address("localhost:27017/test")
        self.assertTupleEqual(expected, result)

    def test_localhost_and_resource(self):
        expected = (None, 'localhost', None, "test", None, None, None)
        result = get_res_address("localhost/test")
        self.assertTupleEqual(expected, result)

    def test_query_string(self):
        expected = (None, 'localhost', None, "test", "query=something&t=1", None, None)
        result = get_res_address("localhost/test?query=something&t=1")
        self.assertTupleEqual(expected, result)

    def test_remote_host_and_resource(self):
        expected = (None, 'domain.com.ar', None, "test", None, None, None)
        result = get_res_address("domain.com.ar/test")
        self.assertTupleEqual(expected, result)

    def test_only_resource(self):
        expected = (None, None, None, 'test', None, None, None)
        result = get_res_address("test")
        self.assertTupleEqual(expected, result)

    def test_full_address_with_ip(self):
        expected = (None, '127.0.0.1', 10001, "test-prod", None, None, None)
        result = get_res_address("127.0.0.1:10001/test-prod")
        self.assertTupleEqual(expected, result)

    def test_port_and_resource(self):
        expected = (None, None, 5000, "test", None, None, None)
        result = get_res_address(":5000/test")
        self.assertTupleEqual(expected, result)

    def test_ip_and_resource(self):
        expected = (None, '192.168.0.5', None, "my_db", None, None, None)
        result = get_res_address("192.168.0.5/my_db")
        self.assertTupleEqual(expected, result)

    def test_scheme_ip_and_resource(self):
        expected = ('mongodb', '192.168.0.5', None, 'my_db', None, None, None)
        result = get_res_address("mongodb://192.168.0.5/my_db")
        self.assertTupleEqual(expected, result)

    def test_scheme_host_and_resource(self):
        expected = ('postgres', 'localhost', None, "my_db", None, None, None)
        result = get_res_address("postgres://localhost/my_db")
        self.assertTupleEqual(expected, result)

    def test_ipv6_address(self):
        expected = (None, '[::10]', None, "foo10", None, None, None)
        result = get_res_address("[::10]/foo10")
        self.assertTupleEqual(expected, result)
        result = get_res_address("[2001:0db8:0000:0000:0000:ff00:0042:8329]/foo10")
        expected = (None, '[2001:0db8:0000:0000:0000:ff00:0042:8329]', None, "foo10", None, None, None)
        self.assertTupleEqual(expected, result)

    def test_scheme_ipv6_address(self):
        expected = ('ftp', '[::10]', None, "foo10", None, None, None)
        result = get_res_address("ftp://[::10]/foo10")
        self.assertTupleEqual(expected, result)

    def test_ipv6_upper_case_address(self):
        expected = (None, '[2001:0DB8:0000:0000:0000:FF00:0042:8329]', None, "TEST", None, None, None)
        result = get_res_address("[2001:0DB8:0000:0000:0000:FF00:0042:8329]/TEST")
        self.assertTupleEqual(expected, result)

    def test_ipv4_mapped_ipv6_address(self):
        expected = (None, '[::ffff:192.168.89.9]', None, "test", None, None, None)
        result = get_res_address("[::ffff:192.168.89.9]/test")
        self.assertTupleEqual(expected, result)

    def test_ipv6_and_port_address(self):
        expected = (None, '[::1]', 9999, "foo", None, None, None)
        result = get_res_address("[::1]:9999/foo")
        self.assertTupleEqual(expected, result)

    def test_basic_auth(self):
        expected = (None, 'localhost', 9999, "foo", None, "user", "pass")
        result = get_res_address("user:pass@localhost:9999/foo")
        self.assertTupleEqual(expected, result)

    def test_basic_auth_ipv4(self):
        expected = (None, '10.0.0.4', None, "foo", None, "user", "pass")
        result = get_res_address("user:pass@10.0.0.4/foo")
        self.assertTupleEqual(expected, result)

    def test_basic_auth_ipv6(self):
        expected = (None, '[::1]', 2222, "foo", None, "user", "pass")
        result = get_res_address("user:pass@[::1]:2222/foo")
        self.assertTupleEqual(expected, result)

    def test_user_but_password(self):
        expected = (None, 'localhost', 9999, "foo", None, "user", None)
        result = get_res_address("user:@localhost:9999/foo")
        self.assertTupleEqual(expected, result)

    def test_user_but_password_and_without_separator(self):
        expected = (None, 'localhost', 9999, "foo", None, "user", None)
        result = get_res_address("user@localhost:9999/foo")
        self.assertTupleEqual(expected, result)

    def test_full_components(self):
        expected = ("mongodb+srv", 'localhost', 9999, "foo", "expire=200", "user", "pass")
        result = get_res_address("mongodb+srv://user:pass@localhost:9999/foo?expire=200")
        self.assertTupleEqual(expected, result)

    def test_auth_with_noalpha_chars_components(self):
        expected = ("mongodb", 'localhost', None, "test", None, "a.b", "p-.$%")
        result = get_res_address("mongodb://a.b:p-.$%@localhost/test")
        self.assertTupleEqual(expected, result)


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
