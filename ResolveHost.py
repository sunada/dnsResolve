#!/usr/bin/python

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
		file.write(IPs[ip]+'	'+ip+'\n')
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
	writeIPs(fw,IPs)

	file.close()

class ThreadClass(threading.Thread):
	def __init__(self,host):
		self.host=host
		threading.Thread.__init__(self)

	def run(self):
		try:
			res=socket.getaddrinfo(self.host,None)
			for re in res:
				print host, re[4][0]
		except Exception, e:
			print e


def MulThreadResolve(fr,fw):
	hosts=ReadHost(fr)
	IPs={}
	threads=[]
	for host in hosts:
		print host
		t=ThreadClass(host)
		threads.append(t)
			
	cntHost=len(hosts)
	for i in range(cntHost):
		threads[i].start()

	for i in range(cntHost):
		threads[i].join()

if __name__=='__main__':
	start=time.time()
	#SynResolve('hosts','IPs')
	MulThreadResolve('hosts','IPs')
	print time.time()-start
