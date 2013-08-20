dnsResolve
==========

use adns to resolve thousands of hosts. You need the liberary of adns and adns-python to run the scripts of asycn_dns.py and resolve_adns.py

(some hosts have both ipv4 and ipv6 addresses.)

example:

./asycn_dns.py hosts_ipv6 hostIPs_asycn_dns 1000 

hosts: a file of hosts

hostIPs: a file to save hosts and their IPs

1000: the intensity. The default value of intensity is 100


example:
./resolve_adns.py hosts_ipv6

hosts_ipv6: a file of hosts which have ipv6 addresses

The script will create a file named hostIP to save the result.
