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
        ans = self.client.expect([pexpect.TIMEOUT, '# '], timeout=30)
        if ans == 0:
            print("ssh has timed out: {}, {}".format(self.client.before, self.client.after))
        elif ans == 1:
            print("ssh connected")
            self.connected = True

    def disconnect(self):
        print("pexpect close goes here")
        self.connected = False

    def add_interface(self, name, vlan, phy, ip, vdom):
        pass

    def add_policy(self, srcintf, dstintf, srcaddr, dstaddr, nat, natpool,
                   action='permit', schedule='always'):
        pass

    def add_address(self, name, subnet):
        pass

    def add_vip(self, name, external, mapped):
        pass
