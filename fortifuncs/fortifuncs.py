#!/usr/bin/python
from getpass import getpass
import pexpect
import os


class FortiGate():
    '''Fancy wrapper to pexpect for FortiGate firewalls'''
    connected = False

    def __init__(self, ip, user=None, passw=None, vdom=None):
        self.ip = ip
        self.vdom = vdom

        if passw is None:
            self.passw = getpass()
        else:
            self.passw = passw

        if user is None:
            self.user = os.getlogin()
        else:
            self.user = user

    def opts(self):
        print(self.ip, self.user, self.passw, self.vdom)

    def connect(self):
        print("ssh to {}@{}".format(self.user, self.ip))
        self.client = pexpect.spawn('ssh {}@{}'.format(self.user, self.ip))
        ans = self.client.expect([pexpect.TIMEOUT, '# '], timeout=5)
        if ans == 0:
            print("connection has timed out")
        elif ans == 1:
            print("connected")
            self.connected = True

    def disconnect(self):
        if self.connected:
            print("closing session")
            self.client.close()
            self.connected = False
        else:
            print("not connected")

    def add_interface(self, name, vlan, phy, ip):
        pass

    def add_policy(self, action, srcintf, dstintf, srcaddr, dstaddr, service,
                   nat=False, natpool=None, schedule='always'):
        pass

    def add_address(self, name, subnet):
        pass

    def add_vip(self, name, external, mapped):
        pass
