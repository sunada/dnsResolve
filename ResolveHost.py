#!/usr/bin/python

import socket

def ReadHost(f1):
	file=open(f1)
	lines=file.readlines()
	
	hosts=[]
	for line in lines:
		line=line.rstrip()
		hosts.append(line)
	file.close()
	return hosts

def SynResolve(fr,fw):
	hosts=ReadHost(fr)
	file=open(fw,'w')
	IPs=[]
	for host in hosts:
		try:
			results=socket.getaddrinfo(host,None)
			for result in results:
				print host, result[4][0]
				file.write(host+'	'+result[4][0]+'\n')
		except Exception,e:
			print e
	file.close()

if __name__=='__main__':
	SynResolve('hosts','IPs')
