#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Custom type validations' tests.

"""
import netaddr
import netifaces
from unittest import main, TestCase

from tinyscript.helpers.types import *

from utils import *


class TestHelpersTypes(TestCase):
    def test_general_purpose_types(self):
        tf = "test_folder"
        tfne = "test_folder_not_existing"
        l1 = ["test1.txt", "test2.txt"]
        l2 = ["test1.txt", "test3.txt"]
        l3 = ["test3.txt", "test4.txt"]
        touch("test1.txt", "test2.txt")
        self.assertEqual(folder_exists_or_create(tf), tf)
        self.assertEqual(file_exists(l1[0]), l1[0])
        self.assertRaises(ValueError, file_exists, l3[0])
        self.assertRaises(ValueError, file_exists, tf)
        self.assertEqual(files_list(l1), l1)
        self.assertRaises(ValueError, files_list, l2)
        self.assertEqual(files_filtered_list(l2), [l2[0]])
        self.assertRaises(ValueError, files_filtered_list, l3)
        self.assertEqual(folder_exists(tf), tf)
        self.assertRaises(ValueError, folder_exists, tfne)
        self.assertRaises(ValueError, folder_exists, l1[0])
        rmdir(tf)
        self.assertEqual(folder_exists_or_create(tfne), tfne)
        self.assertRaises(ValueError, folder_exists_or_create, l1[0])
        self.assertEqual(folder_exists(tfne), tfne)
        rmdir(tfne)
        remove("test1.txt")
        remove("test2.txt")
        self.assertEqual(neg_int(-1), -1)
        self.assertEqual(negative_int(-1), -1)
        self.assertRaises(ValueError, neg_int, 0)
        self.assertRaises(ValueError, neg_int, 1)
        self.assertRaises(ValueError, neg_int, -1.2)
        self.assertRaises(ValueError, neg_int, "test")
        self.assertEqual(pos_int(0), 0)
        self.assertEqual(pos_int(1), 1)
        self.assertEqual(positive_int(1), 1)
        self.assertRaises(ValueError, pos_int, -1)
        self.assertRaises(ValueError, pos_int, 1.2)
        self.assertRaises(ValueError, pos_int, "test")
        self.assertEqual(ints("1,-1"), [1, -1])
        self.assertEqual(ints("[1,-1]"), [1, -1])
        self.assertRaises(ValueError, ints, "0,1]")
        self.assertRaises(ValueError, ints, ["a", 1])
        self.assertEqual(neg_ints("-1"), [-1])
        self.assertEqual(negative_ints("[-1,-2]"), [-1, -2])
        self.assertRaises(ValueError, neg_ints, "-1,-2]")
        self.assertRaises(ValueError, neg_ints, [-1, 1])
        self.assertRaises(ValueError, neg_ints, "-1,0")
        self.assertRaises(ValueError, neg_ints, "test,0")
        self.assertEqual(pos_ints("1"), [1])
        self.assertEqual(positive_ints("[1,2]"), [1, 2])
        self.assertRaises(ValueError, pos_ints, "[1,2")
        self.assertRaises(ValueError, pos_ints, [-1, 1])
        self.assertRaises(ValueError, pos_ints, "test,0")
        self.assertIsNotNone(any_hash("0" * 32))
        self.assertRaises(ValueError, any_hash, "bad_hash")
        self.assertRaises(ValueError, md5_hash, "bad_hash")
        self.assertRaises(ValueError, sha1_hash, "bad_hash")
        self.assertRaises(ValueError, sha224_hash, "bad_hash")
        self.assertRaises(ValueError, sha256_hash, "bad_hash")
        self.assertRaises(ValueError, sha512_hash, "bad_hash")
    
    def test_network_related_types(self):
        self.assertIsNotNone(domain_name("example.com"))
        self.assertRaises(ValueError, domain_name, "bad_name")
        self.assertRaises(ValueError, email_address, "bad_email")
        self.assertRaises(ValueError, email_address, "user@bad_name")
        self.assertIsInstance(ip_address("127.0.0.1"), netaddr.IPAddress)
        self.assertIsInstance(ip_address("12345"), netaddr.IPAddress)
        self.assertIsInstance(ip_address("12345678900"), netaddr.IPAddress)
        self.assertRaises(ValueError, ipv4_address, "12345678900")
        self.assertIsInstance(ip_address("fe00::"), netaddr.IPAddress)
        self.assertRaises(ValueError, ip_address, "0.0.0.300")
        self.assertRaises(ValueError, ipv4_address, "0.0.0.300")
        self.assertRaises(ValueError, ip_address, "fe00:::")
        self.assertRaises(ValueError, ipv6_address, "fe00:::")
        self.assertIsInstance(list(ip_address_list("192.168.1.0/30")), list)
        self.assertRaises(ValueError, ip_address_list, "192.168.1.0.0/24")
        self.assertIsInstance(list(ip_address_network("192.168.1.0/30")), list)
        self.assertRaises(ValueError, ip_address_network, "192.168.1.0.0/24")
        self.assertIsInstance(mac_address(12345), netaddr.EUI)
        self.assertIsInstance(mac_address("01:02:03:04:05:06"), netaddr.EUI)
        self.assertRaises(ValueError, mac_address, "01:02:03-04:05:06")
        self.assertIsInstance(port_number(100), int)
        self.assertRaises(ValueError, port_number, -1)
        self.assertRaises(ValueError, port_number, 123456789)
        self.assertIsInstance(port_number_range(100), int)
        self.assertIsInstance(port_number_range("20-40"), list)
        self.assertRaises(ValueError, port_number_range, -1)
        self.assertRaises(ValueError, port_number_range, 123456789)
        self.assertRaises(ValueError, port_number_range, "40-20")
        GOOD = netifaces.interfaces()[0]
        BAD  = "THIS_INTERFACE_DOES_NOT_EXIST"
        self.assertTrue(network_interface(GOOD))
        self.assertRaises(ValueError, network_interface, BAD)
        AGOOD = list(netifaces.ifaddresses(GOOD).values())[0][0]['addr']
        ABAD  = "THIS_ADDRESS_IS_NOT_VALID"
        self.assertTrue(interface_address(AGOOD))
        self.assertRaises(ValueError, interface_address, BAD)
        self.assertTrue(interface_address_list([AGOOD]))
        self.assertRaises(ValueError, interface_address_list, [BAD])
        self.assertEqual(interface_address_filtered_list([BAD]), [])
        GGOOD = list(netifaces.gateways()['default'].values())
        if len(GGOOD) > 0:
            self.assertTrue(gateway_address(GGOOD[0][0]))
            self.assertTrue(default_gateway_address(GGOOD[0][0]))
        GBAD  = "THIS_GATEWAY_ADDRESS_IS_NOT_VALID"
        self.assertRaises(ValueError, gateway_address, GBAD)
        self.assertRaises(ValueError, default_gateway_address, GBAD)
    
    def test_data_type_check(self):
        self.assertTrue(is_int(1))
        self.assertFalse(is_int("a"))
        self.assertTrue(is_pos_int(10))
        self.assertTrue(is_pos_int(0, True))
        self.assertFalse(is_pos_int(0, False))
        self.assertFalse(is_pos_int(-10))
        self.assertTrue(is_neg_int(-10))
        self.assertFalse(is_neg_int(10))
        self.assertTrue(is_dict({"key": "value"}))
        self.assertFalse(is_dict("not_a_dict"))
        self.assertFalse(is_dict(["not_a_dict"]))
        self.assertTrue(is_list([0]))
        self.assertTrue(is_list((0, )))
        self.assertTrue(is_list({0}))
        self.assertFalse(is_list("not_a_list"))
        self.assertTrue(is_str("test"))
        self.assertFalse(is_str(1))
        self.assertTrue(is_lambda(dummy_lambda))
        self.assertFalse(is_lambda(True))
        self.assertTrue(is_function(dummy_lambda))
        self.assertTrue(is_function(dummy_function))
        self.assertFalse(is_function("not_a_function"))
    
    def test_data_format_check(self):
        self.assertTrue(is_bin("01000111"))
        self.assertFalse(is_bin("0123"))
        self.assertTrue(is_hex("deadbeef"))
        self.assertTrue(is_hex("c0ffee"))
        self.assertFalse(is_hex("coffee"))
        self.assertFalse(is_hex("00a"))
        self.assertTrue(is_md5("0" * 32))
        self.assertTrue(is_hash("0" * 32))
        self.assertTrue(is_sha1("a" * 40))
        self.assertTrue(is_sha224("1" * 56))
        self.assertTrue(is_sha256("b" * 64))
        self.assertTrue(is_sha512("2" * 128))
        self.assertTrue(is_hash("0" * 128))
        self.assertFalse(is_hash("not_a_hash"))
    
    def test_network_format_check(self):
        self.assertTrue(is_domain("example.com"))
        self.assertFalse(is_email("example.com"))
        self.assertTrue(is_email("test@example.com"))
        self.assertTrue(is_ip("1234"))
        self.assertTrue(is_ipv4("1234"))
        self.assertTrue(is_ipv6("12345678900"))
        self.assertFalse(is_ipv4("12345678900"))
        self.assertFalse(is_ipv6("1234567890123456789012345678901234567890123"))
        self.assertTrue(is_ipv6("123456789012345678901234567890123456789"))
        self.assertTrue(is_ip("127.0.0.1"))
        self.assertTrue(is_ipv4("127.0.0.1"))
        self.assertTrue(is_ip("fe00::"))
        self.assertTrue(is_ipv6("fe00::"))
        GOOD = ["1.2.3.4", "fe00::", "127.0.0.0/30"]
        BAD1 = ["1.2.3.300", "fe00::", "127.0.0.0/30"]
        BAD2 = ["1.2.3.4", "fe00::", "127.0.0.0/40"]
        self.assertTrue(all(is_ip(_) for _ in ip_address_list(GOOD)))
        self.assertRaises(ValueError, ip_address_list, BAD1)
        self.assertRaises(ValueError, ip_address_list, BAD2)
        self.assertRaises(ValueError, ipv4_address_list, BAD1)
        self.assertRaises(ValueError, ipv6_address_list, BAD2)
        self.assertTrue(all(is_ip for _ in ip_address_filtered_list(BAD1)))
        self.assertTrue(all(is_ip for _ in ip_address_filtered_list(BAD2)))
        self.assertTrue(all(is_ip for _ in ipv4_address_filtered_list(BAD1)))
        self.assertTrue(all(is_ip for _ in ipv6_address_filtered_list(BAD2)))
        self.assertTrue(is_mac("12345"))
        self.assertTrue(is_mac("01:02:03:04:05:06"))
        self.assertTrue(is_mac("01-02-03-04-05-06"))
        self.assertFalse(is_mac("01:02:03:04:05"))
        self.assertFalse(is_mac("01|02|03|04|05|06"))
        GOOD = netifaces.interfaces()[0]
        BAD  = "THIS_INTERFACE_DOES_NOT_EXIST"
        self.assertTrue(is_netif(GOOD))
        self.assertFalse(is_netif(BAD))
        AGOOD = list(netifaces.ifaddresses(GOOD).values())[0][0]['addr']
        ABAD  = "THIS_ADDRESS_IS_NOT_VALID"
        self.assertTrue(is_ifaddr(AGOOD))
        self.assertFalse(is_ifaddr(ABAD))
        
    
    def test_option_format_check(self):
        self.assertTrue(is_long_opt("--test"))
        self.assertFalse(is_long_opt("-t"))
        self.assertTrue(is_short_opt("-t"))
        self.assertFalse(is_short_opt("--test"))
