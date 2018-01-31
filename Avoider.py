# CLASS AVOIDER

class Avoidance:
		

	def __init__(self,start,cs,MAV):
		
		Safety = 6
		cruise = 16	
		dataPath = 'dlite/flight_information.txt'
		
		self.localizer = movingObs('moving_obstacle_file.txt')


		



		if(start == None):
			self.Home = Locationwp().Set(cs.lat,cs.lng,0, 16)
		else:
			self.Home = start

		self.Bounds = []
		self.addBounds()
		self.printBounds()

		self.StaticObstacles = []
		self.addStaticObstacles()

	def addStaticObstacles(self):
		lngth = file_len_Loc(self.StaticObstacleLoc)
		print lngth
		with open(self.StaticObstacleLoc,"r") as ObSFile:
			for i in range(lngth):
				Obdat = ObSFile.readline().split(" ")
				print Obdat
				temp = self.toPoint2(float(Obdat[1]),float(Obdat[2]),float(Obdat[3]))
				temp.append(float(Obdat[4]))
				self.StaticObstacles.append(temp)

		print self.StaticObstacles


	def getPath(loc,loc2,Moving,timeout):
	if (Moving == False):

	else:



	def getMovingObstacles(self,WPlst,TimeToStart):
		Time = 0	# dist_to_first_wp/self.cruise 

		movObs = self.readMovingObstacles()

		Important_moving_Obs = []
		for i in range(len(WPlst)-1):
			Pos = WPlst[i]
			dx = WPlst[i+1][0]-WPlst[i][0]
			dy = WPlst[i+1][1]-WPlst[i][1]
			dz = WPlst[i+1][2]-WPlst[i][2]
			dis = (dx**2+dy**2+dz**2)**.5

			Vel = [dx*self.cruise/dis,dy*self.cruise/dis,dz*self.cruise/dis]

			Important_moving_Obs.append(self.localizer.closestApproach(Pos,Vel,Time))

		Time = Time + dist_list(WPlst[i],WPlst[i+1])/self.cruise
		# add time based off angle and time it takes turn
		# could be like turn radius/cruise_speed time sin angle

		return ImportantmovObs


	def startSenario(self,wps,moving):
		