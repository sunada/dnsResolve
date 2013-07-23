#!/usr/bin/python

import adns
import sys
import time

def ReadFile(fr):
    hosts=[]
    file=open(fr)
    lines=file.readlines()
    for line in lines:
        hosts.append(line[7:-2])
    file.close()
    return hosts

def WriteFile(fw,ress):
    file=open(fw,'a')
    for res in ress:
        print res[0]
        print ress[res]
        file.write(ress[res]+'		'+res[0]+'\n')
        file.close()

class QueryEngine(object):

    def __init__(self,s=None):
        self._s=s or adns.init(adns.iflags.noautosys)
        self._queries={}
        self.IPhost={}

    def submit(self,qname,rr,flags=0):
        q=self._s.submit(qname,rr,flags)
        self._queries[q]=qname,rr,flags

    def run(self,timeout=0):
        for q in self._s.completed():
            answer=q.check()
            qname,rr,flags=self._queries[q]
            del self._queries[q]
            self.IPhost[answer[3]]=qname
            print qname, '		',answer[3]

    def finished(self):
        return not len(self._queries)

    def getIPhost(self):
        return self.IPhost

def resolveDns(fr,fw):
    hosts=ReadFile(fr)
    start=time.time()
    qe=QueryEngine()
    for host in hosts:
        qe.submit(host,adns.rr.AAAA)

    while not qe.finished():
        qe.run()
	
    print 'time cost:',time.time()-start
    IPhost=qe.getIPhost()
    WriteFile(fw,IPhost)

if __name__=='__main__':
    filename=sys.argv[1]
    resolveDns(filename,'hostIP')
