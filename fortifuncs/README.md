#FortiFuncs

An easy to use module for automating common operations on FortiGate firewalls via SSH.
No FortiManager required. All methods implemented using Pexpect <http://pexpect.readthedocs.org>.

---

###Current Features
  - Adding interfaces
  - Adding VIPs (static and port-forward)
  - Adding Firewall Addresses (Aliases)
  - Adding Firewall Policies
  - VDOM Support


###Available Methods and Arguments
```python
class FortiGate():
    def __init__(self, ip, hostname, user=None, passw=None):
    '''Initialise object with IP and system hostname. System hostname used for expecting
       the prompt. Optional arguments username and password will be taken from user variable 
       and getpass() if not provided.'''

    def status(self):
    '''Prints connection information and current VDOM.'''

    def connect(self, debug=False):
    '''Attempts to SSH to the FortiGate using provided credentials. Turning debug to True
       turns on echoing FortiGate output to STDOUT.'''

    def disconnect(self):
    '''Close SSH session.'''

    def add_interface(self, name, vlan, phy, ip, description=None):
    '''Add new VLAN subinterface. Physical trunk port specified by 'phy' argument.'''

    def add_policy(self, action, srcintf, dstintf, srcaddr, dstaddr, service='ALL',
                   nat=False, ippool=None, schedule='always'):
    '''Add a new firewall policy.'''

    def add_address(self, name, subnet, interface=None):
    '''Add a new address. Optionally bind to interface'''

    def add_vip(self, name, extip, mappedip, extintf='any', extport=None, mappedport=None):
    '''Add a new NAT VIP. If extport is not specified a static one-to-one NAT will be created.'''

    def set_context(self, vdom):
    '''Edit VDOM. Setting VDOM to None will return to global.'''
```

###Example
```python
#!/usr/local/bin/python3.3
import sys
import ipaddress
import fortifuncs


def progress(message):
    sys.stdout.write(message)
    sys.stdout.flush()


if len(sys.argv) != 4:
    print('usage: ./sample.py <network/mask> <vlan> <public>')
    sys.exit(1)

# Firewall Info
ip = '10.0.0.1'
hostname = 'spam'
vdom = 'brian'

subnet = ipaddress.IPv4Network(sys.argv[1])
vlan = sys.argv[2]
public = sys.argv[3]

gateway = str(list(subnet.hosts())[-1]) + '/{}'.format(subnet.prefixlen)
webserver = str(list(subnet.hosts())[0])

customer_int = '{}_{}'.format(vdom, vlan)
subnet_name = 'vlan{}'.format(vlan)
vip_name = 'vlan{}_public'.format(vlan)
pub_int = '{}_wan'.format(vdom)

firewall = fortifuncs.FortiGate(ip, hostname)
firewall.connect()
print('connected')
firewall.set_context(vdom)
progress('editing vdom...')
firewall.add_interface(name=customer_int, ip=gateway, vlan=vlan, phy='port1')
progress('added interface...')
firewall.add_address(name=subnet_name, subnet=str(subnet))
progress('added address...')
firewall.add_vip(name=vip_name, extip=public, mappedip=webserver)
progress('added static nat...')
firewall.add_policy(action='accept', srcintf=customer_int, dstintf=pub_int,
                    srcaddr=subnet_name, dstaddr='all', service='HTTP HTTPS DNS SMTP',
                    nat=True)
progress('added outbound policy...')
firewall.add_policy(action='accept', srcintf=pub_int, dstintf=customer_int,
                    srcaddr='all', dstaddr=vip_name, service='HTTP HTTPS')
progress('added inbound policy...')
print('done!')
```
