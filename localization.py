import math
import time
import threading



class movingObs:
	def __init__(self,fileReadLoc):
		self.fileLoc = fileReadLoc
		self.loger = threading.Thread(target=self.run)
		self.Reading = False
		self.hz = 4.0

		
		self.num = 0
		self.moving_Obstacles = []

		ob_File = open(self.fileLoc,"r")
		Ob_data = ob_File.readline().split(" ")
		while(len(Ob_data) == 7):
			self.num = self.num+1
			temp = dynamics_Ob(self.hz)
			temp.addRadius(float(Ob_data[6]))
			self.moving_Obstacles.append(temp)
			
			Ob_data = ob_File.readline().split(" ")

		ob_File.close()
		
		# make new objects for each file
			

	def start(self):
		self.Reading = True
		self.loger.start()

	def stop(self):
		pass
		self.Reading = False

	# fix this
	def run(self):
		
		while(self.Reading):

			ob_File = open(self.fileLoc,"r")
			for i in range(len(self.moving_Obstacles)):
				Ob_data = ob_File.readline().split(" ")
				if(len(Ob_data) > 1):
					self.moving_Obstacles[i].addLoc( float(Ob_data[0]), float(Ob_data[1]), float(Ob_data[2]))
			ob_File.close()

			sleeptime = 1/self.hz
			print 'sleep: ',sleeptime
			time.sleep(sleeptime)

	def file_len(self):
	    i = 0
	    file = open(self.fileLoc,"r")
	    for line in file:
	    	i += 1
	    file.close()
	    return i

	# returns each object distance, [closest point,radius]
	def closestApproach(self,pos,vel,time):
		closest_approach = []
		closest_dist = []
		for ob in self.moving_Obstacles:
			tempdis,temploc = ob.dcaAddtime(pos,vel,time)
			closest_dist.append(tempdis)
			# temploc.append(ob.Radius)
			closest_approach.append(temploc)
			

		return closest_dist, closest_approach



class dynamics_Ob:
	def __init__(self,hertz):
		self.Radius = 0

		self.xVels = [0,0,0,0,0,0,0,0,0,0]
		self.yVels = [0,0,0,0,0,0,0,0,0,0]
		self.zVels = [0,0,0,0,0,0,0,0,0,0]

		self.Vels = [0,0,0,0,0,0,0,0,0,0]
		self.loc = [0,0,0]

		self.thetas = [0,0,0]
		self.phis = [0,0,0]

		self.top_speed = 0
		self.slow_speed = 1000

		self.fiveSecAvg = 0
		self.thirtySecAvg = 0

		self.hz = hertz

		self.nodes = []
		self.nodesVec = []


	def addRadius(self,rad):
		pass
		self.Radius = rad

	def addLoc(self,X,Y,Z):
		self.xVels.pop()
		self.yVels.pop()
		self.zVels.pop()
		self.xVels.insert(0,(X-self.loc[0])*self.hz)
		self.yVels.insert(0,(Y-self.loc[1])*self.hz)
		self.zVels.insert(0,(Z-self.loc[2])*self.hz)

		temp_V = math.sqrt(((X-self.loc[0])*self.hz)**2 + ((Y-self.loc[1])*self.hz)**2 + ((Z-self.loc[2])*self.hz)**2)
		print 'Vel: ',temp_V
		self.Vels.pop()
		self.Vels.insert(0,temp_V)
		
		if (temp_V < self.slow_speed):
			slow_speed = temp_V
		elif (temp_V > self.top_speed):
			top_speed = temp_V
		

		# signal
		self.fiveSecAvg = sum(self.Vels)/(len(self.Vels))
		# average last 30s
		
		temp_theta = math.atan2(self.yVels[0],self.xVels[0])
		temp_phi = math.atan2(self.zVels[0],(math.sqrt((self.xVels[0])**2+(self.yVels[0])**2)))

		# pop theta list
		self.thetas.pop()
		self.thetas.insert(0,temp_theta)

		# pop phi list
		self.phis.pop()
		self.phis.insert(0,temp_phi)

		# check if it hit a node
		# print self.thetas
		# print self.phis
		if((abs(self.thetas[0] - self.thetas[1]) > math.pi*10/180 or abs(self.thetas[0] - self.thetas[1]) > math.pi*10/180) and (abs(self.thetas[0] - self.thetas[2]) > math.pi*10/180 or abs(self.thetas[0] - self.thetas[2]) > math.pi*10/180)):
			if (self.thetas[1] != 0 and self.thetas[2] != 0  and self.phis[1] != 0 and self.phis[2] != 0):
				self.nodes.append(self.loc)
				self.nodesVec.append([temp_theta,temp_phi])
		
		self.loc = [X,Y,Z]		

	def timeAtClosestApproach(self,Pos1,Vel1,Pos2,Vel2):
		p1 = Pos2[0]-Pos1[0]
		p2 = Pos2[1]-Pos1[1]
		p3 = Pos2[2]-Pos1[2]

		v1 = Vel2[0]-Vel1[0]
		v2 = Vel2[1]-Vel1[1]
		v3 = Vel2[2]-Vel1[2]

		t = -(p1*v1+p2*v2+p3*v3)/(v1**2+v2**2+v3**2)
		return t

	def dca(self,Pos1,Vel1,Pos2,Vel2):

		p1 = Pos2[0]-Pos1[0]
		p2 = Pos2[1]-Pos1[1]
		p3 = Pos2[2]-Pos1[2]

		v1 = Vel2[0]-Vel1[0]
		v2 = Vel2[1]-Vel1[1]
		v3 = Vel2[2]-Vel1[2]

		t = -(p1*v1+p2*v2+p3*v3)/(v1**2+v2**2+v3**2)

		x1 = Pos1[0]+t*Vel1[0]
		y1 = Pos1[1]+t*Vel1[1]
		z1 = Pos1[2]+t*Vel1[2]

		x2 = Pos2[0]+t*Vel2[0]
		y2 = Pos2[1]+t*Vel2[1]
		z2 = Pos2[2]+t*Vel2[2]
		
		loc = [x1,y1,z1]
		loc.append(self.Radius)

		dist = ((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)**.5
		return dist,loc

	def getVel(self):
		x_vel = sum(self.xVels)/len(self.xVels)
		y_vel = sum(self.yVels)/len(self.yVels)
		z_vel = sum(self.zVels)/len(self.zVels)

		return[x_vel,y_vel,z_vel]

	def dcaAddtime(self,Pos,Vel,time):
		
		x_vel = sum(self.xVels)/len(self.xVels)
		y_vel = sum(self.yVels)/len(self.yVels)
		z_vel = sum(self.zVels)/len(self.zVels)
		


		x1 = self.loc[0]-time*x_vel
		y1 = self.loc[1]-time*x_vel
		z1 = self.loc[2]-time*x_vel

		x2 = Pos[0]-time*Vel[0]
		y2 = Pos[1]-time*Vel[1]
		z2 = Pos[2]-time*Vel[2]

		dc,loc = self.dca([x1,y1,z1],[x_vel, y_vel, z_vel],[x2,y2,z2],Vel)
		return dc,loc





# pos = [-150,0,0]
# vel = [16,0,0]


# localizer = movingObs('Flight_Logs/moving_obstacles.txt')
# localizer.start()
# time.sleep(3)
# print localizer.closestApproach(pos,vel,0)
# print localizer.moving_Obstacles[0].fiveSecAvg

# time.sleep(1)
# print localizer.closestApproach(pos,vel,0)
# print localizer.moving_Obstacles[0].fiveSecAvg

# localizer.stop()

