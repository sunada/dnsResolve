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
    except Exception, e:
        print e

class Work(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue=queue
        #self.getQueueItem()
        self.start()
    
    def getQueueItem(self):
        while not self.queue.empty():
            print self.queue.get()
    
    def run(self):
        while True:
            try:
                func,args=self.queue.get(block=False)
                apply(func,(args,))
                #func(args)
                self.queue.task_done()
            except Exception, e:
                print e
                break

class WorkManager(object):
    def __init__(self,hosts,threadMax):
        self.queue=Queue.Queue()
        self.threads=[]
        self.__initWorkQueue(getIP,hosts)
        self.__initThreadPool(threadMax)
        
    def __initWorkQueue(self,func,hosts):
        for host in hosts:
            #print func.__name__, host
            self.queue.put((func,host))
        
    def __initThreadPool(self,threadMax):
        for i in range(threadMax):
            self.threads.append(Work(self.queue))
            
    def checkQueue(self):
        return self.queue.qsize()
                
    def checkComplete(self):
        for thread in self.threads:
            if thread.isAlive():
                thread.join()
        
    
if __name__=='__main__':
	hostFile=sys.argv[1]
	hosts=ReadHost(hostFile)
	#print hosts
	start=time.time()
	print 'start dns. '
	wm=WorkManager(hosts,10)
	wm.checkComplete()
	print 'spending: ',time.time()-start
