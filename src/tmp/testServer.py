import threading,socketserver,time

class requestHandler(socketserver.StreamRequestHandler):
    #currentUserLogin={} #{clientArr:accountName}
    def handle(self):
        requestForUpdate=self.request.recv(1024)
        print(self.client_address)
        while requestForUpdate!='':           
            print(requestForUpdate)
            self.wfile.write(bytes('server reply:{0}'.format(requestForUpdate),
                'ascii')
            )
            requestForUpdate=self.request.recv(1024)
        print('client disconnect')

class broadcastServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':

    server=broadcastServer(('localhost',20000),requestHandler)
    t = threading.Thread(target=server.serve_forever)
    t.daemon=True
    t.start()
    print('server start')
    n=0
    while n<=60:
        print(n)
        n+=1
        time.sleep(1)
    server.socket.close()
