import socket

def resolveUrl(url):
    return socket.getaddrinfo(url,None)
    
if __name__=='__main__':
    url='ipv6.google.com'
    result=resolveUrl(url)
    print result[0][4][0]
