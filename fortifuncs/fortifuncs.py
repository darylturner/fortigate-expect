#!/usr/bin/python
from getpass import getpass
import pexpect
import os
import sys


class FortiGate():
    '''FortiGate framework to pexpect.'''
    connected = False
    vdom = None

    def __init__(self, ip, hostname, user=None, passw=None):
        self.ip = ip
        self.hostname = hostname

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
        print('ssh to {}@{}'.format(self.user, self.ip))
        self.client = pexpect.spawn('ssh {}@{}'.format(self.user, self.ip))
        self.client.logfile = sys.stdout
        i = self.client.expect([pexpect.TIMEOUT, 'you sure you want to continue connecting', 'password: '], timeout=5)
        prompt = self.hostname + ' # '
        if i == 0:
            print('connection failed')
            self.client.close()
        elif i == 1:
            self.client.sendline('yes')
            self.client.expect('password: ')
            self.client.sendline(self.passw)
            self.client.expect(prompt)
            self.connected = True
            print('connected')
        elif i == 2:
            print('sending password')
            self.client.sendline(self.passw)
            i = self.client.expect([prompt, 'denied'])
            if i == 0:
                self.connected = True
                print('connected')
            else:
                print('authentication failed')
                self.client.close()


    def disconnect(self):
        if self.connected:
            print('closing session')
            self.client.close()
            self.connected = False
        else:
            print('not connected')

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
            return
        elif vdom is not None and self.vdom is None:
            self.client.sendline('config vdom')
            self.client.expect(self.hostname + ' \(vdom\) # ')
            self.client.sendline('edit {}'.format(vdom))
            self.client.expect(self.hostname + ' \({}\) # '.format(vdom))
            self.vdom = vdom
            return
        elif vdom is not None and self.vdom is not None:
            self.client.sendline('end')
            self.client.expect(self.hostname + ' # ')
            self.vdom = None
            self.client.sendline('config vdom')
            self.client.expect(self.hostname + ' \(vdom\) # ')
            self.client.sendline('edit {}'.format(vdom))
            self.client.expect(self.hostname + ' \({}\) # '.format(vdom))
            self.vdom = vdom
            return
        elif vdom is None and self.vdom is not None:
            self.client.sendline('end')
            self.client.expect(self.hostname + ' # ')
            self.vdom = None
            return
        else:
            raise(pexpect.EOF)
