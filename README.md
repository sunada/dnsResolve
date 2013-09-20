dnsResolve
==========

use adns to resolve thousands of hosts

example:

./asycn_dns.py hosts hostIPs 1000 8.8.8.8.

hosts: a file of hosts

hostIPs: a file to save hosts and their IPs

1000: the intensity. The default value of intensity is 100

8.8.8.8: nameserver. The default value of nameserver is 202.96.199.133

example:
./resolve_adns.py hosts_ipv6

hosts_ipv6: a file of hosts which have ipv6 addresses

The script will create a file named hostIP to save the result.
