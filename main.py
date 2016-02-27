from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
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
		self.__validate_input()
		self.handle_input()
		self.set_labels()

	def handle_input(self):
		"""
		"Main" function which
		:return:
		"""
		in_address = self.ui.line_IP.text()+'/'+str(self.ui.spin_subnet.value())
		if self.__validate_ip(in_address):  # type: bool
			ip_with_mask = str(in_address)
			self.address = IPAddress(ip_with_mask)

	def set_labels(self):
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

	def __validate_input(self):
		regex = QRegExp()
		regex.setPattern('(^[2][0-5][0-5]|^[1]{0,1}[0-9]{1,2})\.([0-2][0-5][0-5]|[1]{0,1}[0-9]{1,2})\.([0-2][0-5][0-5]|[1]{0,1}[0-9]{1,2})\.([0-2][0-5][0-5]|[1]{0,1}[0-9]{1,2})$')
		validator = QRegExpValidator(regex, self.ui.line_IP)
		self.ui.line_IP.setValidator(validator)

	def __validate_ip(self, in_address: str):
		"""
		Validates if a user finished typing the address
		:param in_address: IP address with subnet mask 192.168.0.1/24
		:return: bool
		"""
		if in_address.count('.') == 3 and len(self.ui.line_IP.text()) >= 7 and str(self.ui.line_IP.text()[-1]) != '.':
			return True


if __name__ == '__main__':

	app = QApplication(sys.argv)
	pysub = PySub()
	pysub.show()
	sys.exit(app.exec_())
