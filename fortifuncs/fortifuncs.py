#!/usr/bin/python
from getpass import getpass
import pexpect
import os
import sys


class FortiGateCLI(Exception):
    pass


class InternalError(Exception):
    pass


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

    def status(self):
        print(self.ip, self.user, self.vdom, self.connected)

    def connect(self, debug=False):
        self.client = pexpect.spawn('ssh {}@{}'.format(self.user, self.ip))
        i = self.client.expect([pexpect.TIMEOUT, 'you sure you want to continue connecting', 'password: '], timeout=5)
        if debug:
            self.client.logfile = sys.stdout
        prompt = self.hostname + ' # '
        if i == 0:
            self.client.close()
            raise InternalError('could not connect to host')
        elif i == 1:
            self.client.sendline('yes')
            self.client.expect('password: ')
            self.client.sendline(self.passw)
            self.client.expect(prompt)
            self.connected = True
        elif i == 2:
            self.client.sendline(self.passw)
            i = self.client.expect([prompt, 'denied'])
            if i == 0:
                self.connected = True
            else:
                self.client.close()
                raise InternalError('authentication failed')

    def disconnect(self):
        if self.connected:
            self.client.close()
            self.connected = False

    def add_interface(self, name, vlan, phy, ip, description=None):
        if '/' not in ip:
            raise InternalError('subnet mask missing from ip argument')

        self.client.sendline('config system interface')
        self.client.expect(self.hostname + ' \(interface\) # ')
        self.client.sendline('edit {}'.format(name))
        self.client.expect(self.hostname + ' \({}\) # '.format(name))
        self.client.sendline('set vlanid {}'.format(vlan))
        self.client.expect(self.hostname + ' \({}\) # '.format(name))
        self.client.sendline('set ip {}'.format(ip))
        self.client.expect(self.hostname + ' \({}\) # '.format(name))

        self.client.sendline('set interface {}'.format(phy))
        i = self.client.expect(['Command fail', self.hostname + ' \({}\) # '.format(name)])
        if i == 0:
            self.client.sendline('abort')
            raise FortiGateCLI(self.client.before)

        if description is not None:
            self.client.sendline('set description {}'.format(description))
            self.client.expect(self.hostname + ' \({}\) # '.format(name))

        if self.vdom is not None:
            self.client.sendline('set vdom {}'.format(self.vdom))
            self.client.expect(self.hostname + ' \({}\) # '.format(name))

        self.client.sendline('end')
        i = self.client.expect(['Command fail', self.hostname + ' \({}\) # '.format(self.vdom)])
        if i == 0:
            raise FortiGateCLI(self.client.before)
        return

    def add_policy(self, action, srcintf, dstintf, srcaddr, dstaddr, service,
                   nat=False, natpool=None, schedule='always'):
        pass

    def add_address(self, name, subnet, interface=None):
        self.client.sendline('config firewall address')
        self.client.expect(self.hostname + ' \(address\) # ')
        self.client.sendline('edit {}'.format(name))
        i = self.expect(['Command fail', self.hostname + ' \({}\) # '.format(name)])
        if i == 0:
            raise FortiGateCLI(self.client.before)

        if '/' not in subnet:
            subnet += '/32'
        self.client.sendline('set subnet {}'.format(subnet))
        self.client.expect(self.hostname + ' \({}\) # '.format(name))

        if interface is not None:
            self.client.sendline('set associated-interface {}'.format(interface))
            i = self.client.expect(['Command fail', self.hostname + ' \({}\) # '.format(name)])
            if i == 0:
                self.client.sendline('abort')
                raise FortiGateCLI(self.client.before)

        self.client.sendline('end')
        i = self.client.expect(['Command fail', self.hostname + ' \({}\) # '.format(self.vdom)])
        if i == 0:
            raise FortiGateCLI(self.client.before)
        return

    def add_vip(self, name, extip, mappedip, extintf='any', extport=None, mappedport=None):
        self.client.sendline('config firewall vip')
        self.client.expect(self.hostname + ' \(vip\) # ')
        self.client.sendline('edit {}'.format(name))
        i = self.client.expect(['Command fail', self.hostname + ' \({}\) # '.format(name)])
        if i == 0:
            raise FortiGateCLI(self.client.before)

        self.client.sendline('set extip {}'.format(extip))
        self.client.expect(self.hostname + ' \({}\) # '.format(name))
        self.client.sendline('set mappedip {}'.format(mappedip))
        self.client.expect(self.hostname + ' \({}\) # '.format(name))
        self.client.sendline('set extintf {}'.format(extintf))
        i = self.client.expect(['Command fail', self.hostname + ' \({}\) # '.format(name)])
        if i == 0:
            self.client.sendline('abort')
            raise FortiGateCLI(self.client.before)

        if extport is not None:
            self.client.sendline('set portforward enable')
            self.client.expect(self.hostname + ' \({}\) # '.format(name))
            self.client.sendline('set extport {}'.format(extport))
            self.client.expect(self.hostname + ' \({}\) # '.format(name))

            if mappedport is not None:
                self.client.sendline('set mappedport {}'.format(mappedport))
                self.client.expect(self.hostname + ' \({}\) # '.format(name))

        self.client.sendline('end')
        i = self.client.expect(['Command fail', self.hostname + ' \({}\) # '.format(self.vdom)])
        if i == 0:
            raise FortiGateCLI(self.client.before)
        return

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
            raise InternalError('inconsistent vdom state')
