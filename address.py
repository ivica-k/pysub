# -*- coding: utf-8 -*-

import sys

try:
	from netaddr import IPNetwork
except ImportError:
	print("Missing netaddr. Install requirements by running 'pip install -r requirements.txt'")
	sys.exit(1)


class IPAddress:
	def __init__(self, input_address=None):
		if input_address:
			self.ip = IPNetwork(input_address).ip
			self.broadcast = IPNetwork(input_address).broadcast
			self.network_address = IPNetwork(input_address).network
			self.subnet_mask = IPNetwork(input_address).netmask
			self.first_address = self.network_address + 1
			self.num_hosts = self.__get_num_hosts(IPNetwork(input_address).size)
			self.binary_subnet_mask = self.subnet_mask.bits()
			self.network_class = self.__get_network_class(input_address)  # type: str
			self.default_subnet = self.__get_default_subnet(input_address)  # type: int

			self.__netmask_sanity_check()

	def __netmask_sanity_check(self):
		"""
		Sets proper values to fields when subnet mask exceeds 31
		:return:
		"""
		if self.broadcast:
			self.last_address = self.broadcast - 1
		else:
			self.broadcast = self.ip
			self.last_address = ""
			self.first_address = ""

	@staticmethod
	def __get_num_hosts(network_size):
		num_hosts = 0

		if network_size >= 2:
			num_hosts = network_size - 2

		return num_hosts

	@staticmethod
	def __get_network_class(input_address):
		threshold = input_address.split('.')[0]

		if int(threshold) <= 127:
			return 'A'
		elif 128 <= int(threshold) < 192:
			return 'B'
		elif int(threshold) >= 192:
			return 'C'

	@staticmethod
	def __get_default_subnet(input_address):
		threshold = input_address.split('.')[0]

		if int(threshold) <= 127:
			return 8
		elif 128 <= int(threshold) < 192:
			return 16
		elif int(threshold) >= 192:
			return 24
