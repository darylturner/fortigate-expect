#!/usr/bin/python
from getpass import getpass
import os


class FortiGate():
	ip = '192.168.1.1'
	user = None
	passw = None

	def __init__(self, ip, user=None, passw=None):
		self.ip = ip
		if passw is None:
			self.passw = getpass()
		if user is None:
			self.user = os.getlogin()

	
	def opts(self):
		print(self.ip, self.user, self.passw)
