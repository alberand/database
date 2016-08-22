import sys,socket,time
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    sock.connect(('localhost',5000))
except socket.error:
    print('connection error')
    sys.exit(0)
n=0
while n<=10:    #connect once
    sock.send(bytes('c1:{0}'.format(n), 'ascii'))
    result=sock.recv(1024)
    print(result)    
    n+=1
    time.sleep(1)
sock.close()

#once you close a socket, you'll need to initialize it again to another socket obj if you want to retransmit
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    sock.connect(('localhost',5000))
except socket.error:
    print('connection error')
    sys.exit(0)
n=0
while n<=10:    #connect once
    sock.send(bytes('c3:{0}'.format(n), 'ascii'))
    result=sock.recv(1024)
    print(result)    
    n+=1
    time.sleep(1)
sock.close()
