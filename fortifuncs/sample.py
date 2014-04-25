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
