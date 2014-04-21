#!/usr/bin/python
from getpass import getpass
import pexpect
import os


class FortiGate():
    '''FortiGate framework to pexpect.'''
    connected = False
    vdom = None

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

    def set_context(self, vdom):
        if vdom is None and self.vdom is None:
            #nothing to do
            return
        elif vdom is not None and self.vdom is None:
            #edit vdom
            pass
        elif vdom is not None and self.vdom is not None:
            #exit current vdom and edit new vdom
            pass
        elif vdom is None and self.vdom is not None:
            #exit current vdom
            pass
        else:
            #this shouldn't of happened!
            raise
