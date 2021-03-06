#!/usr/bin/env python

import sys

try:
	from PyQt5.QtCore import QRegExp
	from PyQt5.QtGui import QRegExpValidator
	from PyQt5.QtWidgets import QMainWindow, QApplication
except ImportError:
	print("Missing PyQt5. Install requirements by running 'pip install -r requirements.txt'")
	sys.exit(1)

from address import IPAddress
from ui.mainwindow import Ui_MainWindow


class PySub(QMainWindow):
	def __init__(self):
		super(PySub, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.address = IPAddress()

		self.run()

	def run(self):
		"""
		Helper function to run all other functions in correct order
		"""
		self.__setup_signals()
		self.__validate_input()
		self.handle_input()

	def __setup_signals(self):
		"""
		QT signals definition
		:return:
		"""
		self.ui.btn_default_subnet.clicked.connect(self.__set_default_subnet)
		self.ui.line_IP.textChanged.connect(self.handle_input)
		self.ui.spin_subnet.valueChanged.connect(self.handle_input)
		self.ui.btn_explain_address_class.clicked.connect(lambda: self.__fill_explanation('address_class'))
		self.ui.btn_explain_net_address.clicked.connect(lambda: self.__fill_explanation('network_address'))
		self.ui.btn_explain_broadcast.clicked.connect(lambda: self.__fill_explanation('broadcast'))
		self.ui.btn_explain_first_node.clicked.connect(lambda: self.__fill_explanation('first_address'))
		self.ui.btn_explain_last_node.clicked.connect(lambda: self.__fill_explanation('last_address'))
		self.ui.btn_explain_subnet_mask.clicked.connect(lambda: self.__fill_explanation('subnet_mask'))
		self.ui.btn_explain_num_ips.clicked.connect(lambda: self.__fill_explanation('num_hosts'))
		self.ui.action_quit.triggered.connect(self.closeApp)

	def handle_input(self):
		"""
		Handles IP address input
		:return:
		"""
		in_address = "%s/%s" % (self.ui.line_IP.text(), self.ui.spin_subnet.value())
		if self.__validate_input():  # type: bool
			self.address = IPAddress(in_address)
			self.__set_labels()

	def __set_labels(self):
		"""
		Sets values for all labels
		:return:
		"""
		self.ui.lab_network_class.setText(str(self.address.network_class))
		self.ui.lab_broadcast_address.setText(str(self.address.broadcast))
		self.ui.lab_first_address.setText(str(self.address.first_address))
		self.ui.lab_last_address.setText(str(self.address.last_address))
		self.ui.lab_network_address.setText(str(self.address.network_address))
		self.ui.lab_num_ips.setText(str(self.address.num_hosts))
		self.ui.lab_subnet_mask.setText(str(self.address.subnet_mask))

	def __set_default_subnet(self):
		"""
		Sets the default subnet
		:return:
		"""
		self.ui.spin_subnet.setValue(self.address.default_subnet)

	def __validate_input(self):
		"""
		Applies a regular expression to QLineEdit field and validates IPv4
		:return:
		"""
		regex = QRegExp()
		regex.setPattern(
			'(^[2][0-5][0-5]|^[1]{0,1}[0-9]{1,2})\.([0-2][0-5][0-5]|[1]{0,1}[0-9]{1,2})\.'
			'([0-2][0-5][0-5]|[1]{0,1}[0-9]{1,2})\.([0-2][0-5][0-5]|[1]{0,1}[0-9]{1,2})$')
		validator = QRegExpValidator(regex, self.ui.line_IP)
		self.ui.line_IP.setValidator(validator)

		state = validator.validate(self.ui.line_IP.text(), 0)[0]

		if state == validator.Acceptable:
			return True

	def __generate_explanation(self, input_property):
		"""
		Generates explanation text for an input_property which corresponds to a property of self.address object
		:param input_property: str
		:return:
		"""
		first_octet = str(self.address.ip).split('.')[0]
		free_bits = str(32 - self.ui.spin_subnet.value())
		available_addresses = 2 ** int(free_bits) - 2
		number_of_subnets = 256 // 2 ** int(free_bits)

		ip = str(self.address.ip).split('/')[0].split('.')

		subnet_ranges = []
		for i in range(0, 255, self.address.num_hosts + 2):
			subnet_ranges.append(
				'%s.%s.%s.%s - %s.%s.%s.%s' %
				(ip[0], ip[1], ip[2], i, ip[0], ip[1], ip[2], i + self.address.num_hosts + 1))

		ranges = self.__get_str_ranges(subnet_ranges)

		explanations = {
			'address_class': '''<p>Network address class is determined by the value of the first segment following
			these simple rules:<p>
			<ul>
			<li>1 - 126: class <strong>A</strong></li>
			<li>128 - 191: class <strong>B</strong></li>
			<li>192 - 223: class <strong>C</strong></li>
			</ul>
			<p>Since the value of the first octet is <strong>''' + first_octet + '''</strong> we determined that the network class
			is <strong>''' + self.address.network_class + '''</strong></p>''',

			'network_address': '''<p>Network address value is determined by the subnet mask value,
			 /''' + str(self.ui.spin_subnet.value()) + ''' in our case. Maximum subnet mask value is /32, which means
			  that there are ''' + free_bits + ''' bits free.
				<br /><br />IP addressing is based on the binary system so we can easily calculate the number of available
			  addresses with ''' + free_bits + ''' free bits:
			  <br /><br />2<sup>''' + free_bits + '''</sup> - 2 = ''' + str(available_addresses) + '''
				<br /><br />Two is substracted because two addresses are reserved; one for broadcast traffic and one for
				network address. Dividing number of free IPs with the value from above gives us the number of subnets,
			  which is ''' + str(number_of_subnets) + ''' in this case. Subnet range(s):
				<br /><br />''' + ranges + '''</p>''',

			'broadcast': '''<p>A broadcast address is a logical address at which all devices connected to a network are enabled to receive data packets.
			<br /><br />Determining broadcast address is not difficult if we know the network address, which is ''' + str(
				self.address.network_address) + '''
			<br /><br />Broadcast is the last address in the given network, which in our case is <strong>''' + str(
				self.address.broadcast) + '''</strong></p>''',

			'first_address': '''<p>First usable address is determined by adding one (1) to the network address.
			<br /><br />First usable address in this case is <strong>''' + str(
				self.address.first_address) + '''</strong></p>''',

			'last_address': '''<p>Last usable address is determined by substracting one (1) from the broadcast address.
			<br /><br />Last usable address in this case is <strong>''' + str(
				self.address.last_address) + '''</strong></p>''',

			'subnet_mask': '''<p>A subnet mask (or number) is used to determine the number of bits used for the subnet and host portions of the address. The mask is a 32-bit value that uses one-bits for the network and subnet portions and zero-bits for the host portion. Binary, this number looks like this:
			<br /><br /><strong>''' + str(self.address.binary_subnet_mask) + '''</strong>
			<br /><br />Converting this binary number to a decimal gives us the subnet mask <strong>''' + str(
				self.address.subnet_mask) + '''</strong></p>''',

			'num_hosts': '''<p>Number of hosts in a network is calculated using this formula
			<br /><br />2<sup>BL</sup> - 2
			<br /><br />
			where BL is the number of bits left when current subnet mask (''' + str(self.ui.spin_subnet.value()) + ''')
			is substracted from 32.</p><p>BL = 32 - ''' + str(self.ui.spin_subnet.value()) + '''</p>
			<p>BL = ''' + str(free_bits) + '''</p>Additionally, 2 is substracted because network address
			and broadcast address are not usable for hosts, leaving us with the final calculation:
			<p>2<sup>''' + str(free_bits) + '''</sup> - 2 = <b>''' + str(self.address.num_hosts) + '''</b></p>'''
		}

		return explanations[input_property]

	@staticmethod
	def __get_str_ranges(ranges):
		"""
		Returns string with newlines from input list of subnet ranges
		:param ranges: list
		:return:
		"""
		ret_value = ''

		for subnet_range in ranges:
			ret_value += str(subnet_range) + '<br />'

		return ret_value

	def __fill_explanation(self, input_property):
		"""
		Fills the text input box with HTML preformatted text
		:param input_property: str
		:return:
		"""
		explanation = self.__generate_explanation(input_property)
		self.ui.text_explanation.setHtml(explanation)

	def closeApp(self):
		QApplication.quit()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	pysub = PySub()
	pysub.show()
	sys.exit(app.exec_())
