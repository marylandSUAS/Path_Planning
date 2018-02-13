import threading

class logger:
	def __init__(self,currentState,cordSystem,file):
		self.running = False
		self.loger = threading.Thread(target=self.log)
		self.textfile = file
		self.cord_System = cordSystem
		self.cs = currentState

	def startlogging(self):
		self.running = True
		self.loger1.start()
		print "Logging Data"

	def stoplogging(self):
		self.running = False
		print('Stopped logging')

	def log(self):
		senarioFile = open(self.textfile,"w")

		while(self.running):
			senarioFile.write(str('\n'))
			point = self.cord_System.toMeters([cs.lat,cs.lng,cs.alt])
			senarioFile.write(str(point[0]))
			senarioFile.write(str(' '))
			senarioFile.write(str(point[1]))
			senarioFile.write(str(' '))
			senarioFile.write(str(point[2]))
			Script.Sleep(250)
			
		senarioFile.close()