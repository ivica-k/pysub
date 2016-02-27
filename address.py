# -*- coding: utf-8 -*-

from netaddr import *

class IPAddress():
	def __init__(self, input_address=None):
		'''
		Prikaz upotrebe klase iz posebnog modula. Nema velike potrebe za ovim, ali je program pisan u edukativne svrhe
		 pa ne škodi
		'''
		if input_address:
			self.ip = IPNetwork(input_address).ip
			self.broadcast = IPNetwork(input_address).broadcast
			self.network_address = IPNetwork(input_address).network
			self.subnet_mask = IPNetwork(input_address).netmask
			self.first_address = self.network_address + 1
			self.last_address = self.broadcast - 1
			self.num_hosts = IPNetwork(input_address).size - 2
			self.network_class = self.__get_network_class(input_address)

	def __get_network_class(self, input_address):
		threshold = input_address[0:3].replace('.','')

		if int(threshold) <= 127:
			return 'A'
		elif int(threshold) >= 128 and int(threshold) < 192:
			return 'B'
		elif int(threshold) >= 192:
			return 'C'