import socket, time

class IOSingleton:
    # Here will be the instance stored.
    __instance = None
    sock = None
    server_address = ('0.0.0.0', 1024)
    conn = None
    addr = None
    connected = False

    @staticmethod
    def getInstance():
        """ Static access method. """
        if IOSingleton.__instance == None:
            IOSingleton()

        return IOSingleton.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if IOSingleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            IOSingleton.__instance = self
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(('0.0.0.0', 1024))

    def connect(self):
        print("Listening for connection on " + socket.gethostname())
        self.sock.listen(0)
        self.conn, self.addr = self.sock.accept()
        self.connected = True
        self.send("connected")
        print(self.addr)
        return True

    def receive(self):
        if self.connected:
            try:
                return self.conn.recv(1024).decode('utf-8')
            except:
                self.connected = False

    def send(self, msg):
        tmp = 'mgr'+msg+'\n'
        try:
            self.conn.send(tmp.encode('utf-8'))
        except:
            self.connected = False

    def close(self):
        self.conn.close()