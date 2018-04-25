import socket
import threading
import subprocess
import socket
import time





class location_Socket:
    def __init__(self,current_State):
        self.host = "192.168.1.2"
        self.port = 8450

        self.run = False
        self.cs = current_State

        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((host, port))

        
        self.sender = threading.Thread(target=self.Sender)

        self.sender.start()

        

        

    def stop(self):
        self.run = False

    def Sender(self):
        # wait for connection with string connected
        server_socket.listen(1)
        conn, addr = server_socket.accept()
        print ('Connected by', addr)


        time_start = time.clock()

        

        while(True and time.clock()-time_start < 60*40):
            red = self.serversocket.recv(1024)#.decode()
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



