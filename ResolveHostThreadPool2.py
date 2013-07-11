#!/usr/bin/python

import sys
import Queue
import threading
import time
import socket

def ReadHost(file):
	f=open(file)
	hosts=[]
	lines=f.readlines()
	for line in lines:
		hosts.append(line[7:-2])
	f.close()
	return hosts

def WriteHost(file,ips):
	f=open(file,'a')
	for ip in ips:
		f.write(ip[1]+'         '+ip[0]+'\n')
	f.close()
    

def getIP(host):
	try:
		res=socket.getaddrinfo(host,None)
		for item in res:
			print host, item[4][0]
			#pass
	except Exception, e:
		print 'getIP',e

class Work(threading.Thread):
	def __init__(self,func,args):
		threading.Thread.__init__(self)
		self.func=func
		self.args=args
		#self.getQueueItem()

	def getQueueItem(self):
		while not self.queue.empty():
			func,args=self.queue.get()
			print func.__name__
			print args

	def run(self):
		try:
			apply(self.func,(self.args,))
			#func(args)
		except Exception, e:
			print 'run',e

class WorkManager(object):
	def __init__(self,func,hosts,threadMax):
		self.queue=Queue.Queue()
		self.threads=[]
		self.threadMax=threadMax
		self.__initWorkQueue(func,hosts)
		self.__initThreadPool(self.threadMax)
		self.__startThread()
    
	def __initWorkQueue(self,func,hosts):
		for host in hosts:
			#print func.__name__, host
			self.queue.put((func,host))
		#print 'in initWorkQueue()'
		#self.getQueueItem()
        
	def __initThreadPool(self,threadMax):
		#self.getQueueItem()

		for i in range(threadMax):
			try:
				func,args=self.queue.get(block=False)
				t=Work(func,args)
				self.threads.append(t)
			except Exception,e:
				print 'workmanager',e
		
	#test whether the queue is right
	def getQueueItem(self):
		qtmp=self.queue
		while not qtmp.empty():
			print qtmp.get()

	def __startThread(self):
		for thread in self.threads:
			thread.start()
            
	def checkQueue(self):
		return self.queue.qsize()
                
	def checkComplete(self):
		for thread in self.threads:
			if thread.isAlive():
				thread.join()
        
	def checkFinished(self):
		qsize=self.checkQueue()
		while qsize:
			print self.checkQueue()
			self.checkComplete()
			self.__initThreadPool(self.threadMax)
			qsize=self.checkQueue()				
			
  
if __name__=='__main__':
	hostFile=sys.argv[1]
	hosts=ReadHost(hostFile)
	#print hosts
	start=time.time()
	print 'start dns. '
	wm=WorkManager(getIP,hosts,10)
	wm.checkFinished()

	print 'spending: ',time.time()-start
