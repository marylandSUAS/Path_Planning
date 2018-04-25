import socket
import threading
import socket
import time





class imageSocket:
    def __init__(self,current_State):
        self.host = "192.168.1.2"
        self.port = 8450

        self.time_log = [0]*20
        self.lat_log = [0]*20
        self.lng_log = [0]*20
        self.yaw_log = [0]*20

        
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.connect((host, port))

        
        self.reader = threading.Thread(target=self.Reader)
        self.reader.start()

        

        

    def stop(self):
        self.run = False

    def Reader(self):
        
        sent = self.serversocket.send(data)
        
        # wait for connection with string connected
        server_socket.listen(1)
        conn, addr = server_socket.accept()
        print ('Connected by', addr)


        time_start = time.clock()
        

        while(True and time.clock()-time_start < 60*40):
            red = self.serversocket.recv(2048)#.decode()
            if(red == 'Start')
                break

        time_start = time.clock()
        while(self.run == True):
            temp_time = time.clock()-time_start
            lat = self.cs.lat
            lng = self.cs.lng
            yaw = self.cs.yaw
            data = str(temp_time)+" "+str(lat)+" "+str(lng)+" "+str(yaw)
            sent = self.serversocket.send(data)#.decode()
            print 'sent bytes: ',sent
            time.sleep(.25)

            if(self.run == False or temp_time > 30*60):
                break



