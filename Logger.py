import threading
import time

class logger:
	def __init__(self,currentState,cordSystem,file,movingObstacles,staticObstacles_file):
		self.running = False
		self.loger = threading.Thread(target=self.log)
		self.textfile = file
		self.cord_System = cordSystem
		self.cs = currentState
		self.moving_Obs = movingObstacles
		self.static_Obstacles = staticObstacles_file

	def startlogging(self):
		self.running = True
		self.loger.start()
		print ("Logging Data")

	def stoplogging(self):
		self.running = False
		print ('Stopped logging')

	def log(self):
		senarioFile = open(self.textfile,"w")

		statics = []
		with open(self.static_Obstacles,"r") as OFile:
			dat = OFile.readline().split(" ")
			while(len(dat) == 4):

				temp = self.cord_System.toMeters([float(dat[0]),float(dat[1]),float(dat[2])])
				temp.append(float(dat[3]))
				statics.append(temp)
				dat = OFile.readline().split(" ")
				

		if(self.static_Obstacles != None):
			for ob in statics:
				senarioFile.write('Static')
				senarioFile.write(str(' '))
				senarioFile.write(str(ob[0]))
				senarioFile.write(str(' '))
				senarioFile.write(str(ob[1]))
				senarioFile.write(str(' '))
				senarioFile.write(str(ob[2]))
				senarioFile.write(str(' '))
				senarioFile.write(str(ob[3]))
				senarioFile.write(str('\n'))



		while(self.running):
			point = self.cord_System.toMeters([self.cs.lat,self.cs.lng,self.cs.alt])
			senarioFile.write(str(point[0]))
			senarioFile.write(str(' '))
			senarioFile.write(str(point[1]))
			senarioFile.write(str(' '))
			senarioFile.write(str(point[2]))

			
			if(self.moving_Obs != None):
				for ob in self.moving_Obs:
					senarioFile.write(str(' '))
					senarioFile.write(ob.radius)
					senarioFile.write(str(' '))
					senarioFile.write(ob.loc(0))
					senarioFile.write(str(' '))
					senarioFile.write(ob.loc(1))
					senarioFile.write(str(' '))
					senarioFile.write(ob.loc(2))
			

			time.sleep(.25)
			senarioFile.write(str('\n'))
					
		senarioFile.close()