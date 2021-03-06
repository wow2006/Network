import socket, time, sys
from chatUI import *


class recvThread(QThread):
    def __init__(self,conn,parent = None):
        QThread.__init__(self,parent)
        self.message = ''
        print("recv thread init")
        self.conn = conn
    
    def run(self):
        print("run threading")
        while 1:
            time.sleep(1)
            self.message = self.conn.recv(1024)
            if not self.message == '': 
                self.emit(SIGNAL("getmessage(QString)"),self.message)
                self.message = ''
                print "Singal is emitted"
                
    def __del__(self):
        self.quit()
            

class ClientConnection(QObject):
    def __init__(self,host,port = 8888):
        self.host = host
        self.port = port
        self.initConnection()
        self.initGUI = MyClass("Ahmed","Hussein")
        self.connect(self.initGUI,SIGNAL("sendMessage(QString)"),self.sendmessage)
        self.connect(self.recThread,SIGNAL("getmessage(QString)"),self.getmessage)
        
    def initConnection(self):
        try:
            # create an INET, STREAMing socket
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.host, self.port))
            self.recThread = recvThread(self.s)
            self.recThread.start()
            print "Connect"
        except socket.error:
            print 'Failed to create socket'
            sys.exit()
            
    def sendmessage(self,message):
        self.s.sendall(message)
        print "message send"
        
    def getmessage(self,message):
        self.initGUI.getmessage(message)
        
    def __del__(self):
        print "colse connection"
        self.s.close()

            
def main():
    app = QApplication(sys.argv)
    start = ClientConnection('localhost')
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()