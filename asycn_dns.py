#########################################
#
# auther: Peteris Krumins
# website: www.catonmat.net/blog/asynchronous-dns-resolution/
#
############################################


#!/usr/bin/python
#

import adns
import sys
import re
from time import time

class AsyncResolver(object):
    def __init__(self, hostsfile,hostIPfile,intensity=100,nameserver='202.96.199.133'):
        """
        hostsfile: file of hosts waiting to be resolved
	hostIPfile: file of hosts and their IPs 
        intensity: how many hosts to resolve at once
	nameserver: dns server
        """
        self.hosts = open(hostsfile)
	self.hostIP = open(hostIPfile,'a')
        self.intensity = intensity
        #self.adns = adns.init(adns.iflags.noautosys,sys.stderr,"nameserver 202.96.199.133")
        self.adns = adns.init(adns.iflags.noautosys,sys.stderr,"nameserver "+nameserver)
	self.hostCnt=0
	self.ipCnt=0

    def get_hosts(self,lines):
	hosts=[]
	for line in lines:
	    line=line.rstrip()
	    pattern=re.compile(r'//.+?/')
	    hosts.append(pattern.findall(line)[0][2:-1])
	return hosts

    def resolve(self):
        def collect_results(tmp):
            #print self.adns.completed()
	    for query in self.adns.completed():
		#print 'the loop in collect_results'
		#print tmp
                answer = query.check()
                host = active_queries[query]
		del active_queries[query]

                if answer[0] == 0:
                    ip = answer[3][0]
                    resolved_hosts[host] = ip
                    self.ipCnt+=len(answer[3])
		    self.hostIP.write(host+'			IP:')
		    self.hostCnt+=1
		    print self.hostCnt,host,ip
		    for item in answer[3]:
		    	self.hostIP.write(item+'	')
		    self.hostIP.write('\n')
		elif answer[0] == 101: # CNAME
                    query = self.adns.submit(answer[1], adns.rr.A)
                    active_queries[query] = host
                else:
                    resolved_hosts[host] = None
		    self.hostIP.write(host+'	'+'None\n')
		    self.hostCnt+=1
		    print self.hostCnt,host,'None'

	def finished_resolving(resolved_hosts,hosts):
		return len(resolved_hosts)==len(hosts)

	while True:
	    cnt=1
#	    print cnt
	    lines=[]
	    resolved_hosts = {}
            active_queries = {}
	    #print 'self.intensity:'+str(self.intensity)

	    lines=self.hosts.readlines()
	    hosts=self.get_hosts(lines)
	    tmp=0
	    resolved_hostCnt=0
	    while not finished_resolving(resolved_hosts,lines):
		tmp+=1
		while hosts and len(active_queries)<self.intensity:
		    host=hosts.pop() 
		    query=self.adns.submit(host,adns.rr.A)
		    active_queries[query]=host
		collect_results(tmp)
	    #print 'line: after collect_results:'+line
	    break 
	self.hosts.close()
	self.hostIP.close()
	return self.hostCnt,self.ipCnt				
	
if __name__ == "__main__":

    #hosts=sys.argv[1]
    #hostIP=sys.argv[2]
    #intensity=sys.argv[3]
    hosts = ['www.sina.com']
    hostIP = 'abc'
    intensity = '100'
    ar = AsyncResolver(hosts,hostIP,int(intensity))
    start = time()
    hostCnt,ipCnt = ar.resolve()  
    end = time()
    print 'ipCnt',
    print ipCnt
    result='It took %.2f seconds to resolve %d hosts and get %d ips' %(end-start,hostCnt,ipCnt)
    print result 
    file=open(hostIP,'a')
    file.write(result+'\n')
    file.close()
