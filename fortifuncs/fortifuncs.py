#!/usr/bin/python
from getpass import getpass
import pexpect
import os


class FortiGate():
	'''Fancy wrapper to pexpect for FortiGate firewalls'''
	ip = None
	user = None
	passw = None
	connected = False

	def __init__(self, ip, user=None, passw=None):
		self.ip = ip
		if passw is None:
			self.passw = getpass()
		else:
			self.passw = passw

		if user is None:
			self.user = os.getlogin()
		else:
			self.user = user

	
	def opts(self):
		print(self.ip, self.user, self.passw)

	
	def connect(self):
		print("pexpect spawn code goes here")
		print("ssh to {}@{}".format(self.user, self.ip))
		self.connected = True

	
	def disconnect(self):
		print("pexpect close goes here")
		self.connected = False

	
	def add_policy(self, srcintf, dstintf, srcaddr, dstaddr, action='permit',
		       schedule='always', nat, natpool):
		pass


	def add_address(self, name, subnet):
		pass


	def add_vip(self, name, external, mapped):
		pass
