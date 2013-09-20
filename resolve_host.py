##########################################################
# author: Ada Sun
# date: 2013/8/20
# function: using multi-thread and socket.getaddrinfo() to resolve hosts
############################################################


#!/usr/bin/python

import sys
import socket
import time 
import threading
import Queue

#MAX_THREAD 20

def ReadHost(f):
	file=open(f)
	lines=file.readlines()
	
	hosts=[]
	for line in lines:
		line=line.rstrip()
		hosts.append(line[7:-1])
	file.close()
	return hosts

def WriteIPs(f,IPs):
	file=open(f,'a')
	for ip in IPs:
		file.write(ip[1]+'		'+ip[0]+'\n')
	file.close()


def SynResolve(fr,fw):
	hosts=ReadHost(fr)
	IPs={}
	for host in hosts:
		try:
			results=socket.getaddrinfo(host,None)
			for result in results:
				print host, result[4][0]
				IPs[result[4][0]]=host
		except Exception,e:
			print e
	WriteIPs(fw,IPs)


class ThreadClass(threading.Thread):
	def __init__(self,host):
		self.host=host
		threading.Thread.__init__(self)

	def run(self):
		global IPhost
		try:
			res=socket.getaddrinfo(self.host,None)
			if mutex.acquire(1):
				for re in res:
					#self.IPhost[re[4][0]]=self.host
					IPhost[re[4][0]]=self.host
				mutex.release()
		except Exception, e:
			print self.host, e
			#pass


def MulThreadResolve(fr):
	#start=time.ctime()
	print 'starting MulThreadResolve at: ',start
	hosts=ReadHost(fr)
	threads=[]
	for host in hosts:
		t=ThreadClass(host)
		threads.append(t)
			
	cntHost=len(hosts)
	for i in range(cntHost):
		threads[i].start()

	for i in range(cntHost):
		threads[i].join()

	#print 'ending MulThreadResolve at :', ctime()

def CntHost(IPhost):
	host={}
	for ip in IPhost:
		host[IPhost[ip]]=1
	return len(host)

if __name__=='__main__':
	#'''
	#resolve hosts one by one
	start=time.time()
	SynResolve('hosts','IPs')
	print 'time cost:',time.time()-start
	#'''

	'''
	#each thread resolve one host
	start=time.time()
	IPhost={}
	mutex=threading.Lock()
	hostFile=sys.argv[1]
	MulThreadResolve(hostFile)
	print CntHost(IPhost)
	res=sorted(IPhost.iteritems(),key=lambda d:d[1],reverse=True)
	WriteIPs('IPhost',res)
	#print res
	#for item in res:
	#	print item[1],' ',item[0]
	print 'time cost:',time.time()-start
	'''

