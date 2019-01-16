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


import unittest
from res_address import *


class TestAddresses(unittest.TestCase):

    def test_full_address(self):
        host, port, resource = get_res_address("localhost:27017/test")
        self.assertEqual(host, 'localhost')
        self.assertEqual(port, 27017)
        self.assertEqual(resource, "test")

    def test_localhost_and_resource(self):
        host, port, resource = get_res_address("localhost/test")
        self.assertEqual(host, 'localhost')
        self.assertIsNone(port)
        self.assertEqual(resource, "test")

    def test_remotehost_and_resource(self):
        host, port, resource = get_res_address("domain.com.ar/test")
        self.assertEqual(host, 'domain.com.ar')
        self.assertIsNone(port)
        self.assertEqual(resource, "test")

    def test_only_resource(self):
        host, port, resource = get_res_address("test")
        self.assertIsNone(host)
        self.assertIsNone(port)
        self.assertEqual(resource, 'test')

    def test_full_address_with_ip(self):
        host, port, resource = get_res_address("127.0.0.1:10001/test-prod")
        self.assertEqual(host, '127.0.0.1')
        self.assertEqual(port, 10001)
        self.assertEqual(resource, "test-prod")

    def test_port_and_resource(self):
        host, port, resource = get_res_address(":5000/test")
        self.assertIsNone(host)
        self.assertEqual(port, 5000)
        self.assertEqual(resource, "test")

    def test_ip_and_resource(self):
        host, port, resource = get_res_address("192.168.0.5/my_db")
        self.assertEqual(host, '192.168.0.5')
        self.assertIsNone(port)
        self.assertEqual(resource, "my_db")

    def test_ipv6_address(self):
        host, port, resource = get_res_address("[::10]/foo10")
        self.assertEqual(host, '[::10]')
        self.assertIsNone(port)
        self.assertEqual(resource, "foo10")

    def test_full_ipv6_address(self):
        host, port, resource = get_res_address("[::1]:9999/foo")
        self.assertEqual(host, '[::1]')
        self.assertEqual(port, 9999)
        self.assertEqual(resource, "foo")


class TestWrongAddresses(unittest.TestCase):

    def test_invalid_port(self):
        self.assertRaises(InvalidPortError, get_res_address, "localhost:NotANumber/test")

    def test_empty_host(self):
        self.assertRaises(InvalidHostError, get_res_address, "/test")

    def test_invalid_host(self):
        self.assertRaises(InvalidHostError, get_res_address, "!/test")
        self.assertRaises(InvalidHostError, get_res_address, "!qwerty/test")

    def test_not_resource(self):
        self.assertRaises(NotResourceProvidedError, get_res_address, "test/")
        self.assertRaises(NotResourceProvidedError, get_res_address, "localhost:123/")

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
