# CLASS AVOIDER

class Avoidance:
		

	def __init__(self,start,cs,MAV,cord_System):
		
		Safety_Margin = 6
		cruise = 16	
		dataPath = 'dlite/flight_information.txt'
		self.cordSystem = cord_System

		self.Index = 1

		self.Home = start


		self.Bounds = []
		self.addBounds('dlite/Boundry_File.txt')

		self.StaticObstacles = []
		self.addStaticObstacles('dlite/Static_file.txt')

		self.localizer = movingObs('dlite/moving_obstacle_file.txt')

	def file_len_Loc(self,fileLoc):
    	i = 0
	    with open(fileLoc,"r") as file:
		    for line in file:
		    	i += 1
	    #print "file length is ", i
	    return i

	def addStaticObstacles(self,static_file):
		lngth = self.file_len_Loc(static_file)

		with open(static_file,"r") as OFile:
			for i in range(lngth):
				dat = OFile.readline().split(" ")
				
				temp = self.cordSystem.toMeters([float(dat[1]),float(dat[2]),float(dat[3])])

				temp.append(float(dat[4]))
				self.StaticObstacles.append(temp)

		# print self.StaticObstacles

	def addBounds(self,bounds_file):
		lngth = self.file_len_Loc(bounds_file)

		with open(bounds_file,"r") as BFile:
			for i in range(lngth):
				dat = BFile.readline().split(" ")
				
				temp = self.cordSystem.toMeters([float(dat[1]),float(dat[2]),float(dat[3])])

				self.Bounds.append(temp)

		# print self.StaticObstacles

	def getMovingObstacles(self,WPlst,TimeToStart):
		Time = 0	# dist_to_first_wp/self.cruise 

		Important_moving_Obs = []
		# Steps through each dis between wps and looks for collisions
		for i in range(len(WPlst)-1):
			Pos = WPlst[i]
			dx = WPlst[i+1][0]-WPlst[i][0]
			dy = WPlst[i+1][1]-WPlst[i][1]
			dz = WPlst[i+1][2]-WPlst[i][2]
			dis = (dx**2+dy**2+dz**2)**.5

			Vel = [dx*self.cruise/dis,dy*self.cruise/dis,dz*self.cruise/dis]

			Important_moving_Obs.append(self.localizer.closestApproach(Pos,Vel,Time))

			Time = Time + dis/self.cruise
			# add time based off angle and time it takes turn
			# could be like turn radius/cruise_speed time sin angle

		return ImportantmovObs

	def start():
		plan(@global_index,wp_list)
	
	#updates vehicle_wps and sends to plane
	def set_vehicle_waypoints(self,wps):
		MAV.setWPTotal(len(lst)+1)	
		MAV.setWP(Locationwp().Set(self.Home[0],self.Home[1],self.Home[2], 16),0,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
		for i in range(len(lst)):
			MAV.setWP(Locationwp().Set(wps[i][0],wps[i][1],wps[i][2], 16),1+i,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
			if (i+1 == 1):
				MAV.setWPCurrent(1)	
		MAV.setMode("Auto")


	

	def get_current_index(self):
		pass
		return self.Index

	def plan(self,index,wp_list):
		if (index == size(wp_list)-1):
			return
		while(distance to wp_list[index] > TBD [m]):
			time.sleep(.1)

		Store DL_1(wp_list[index],wp_list[index + 1], only static)
		DL_1(wp_list[index],wp_list[index + 1])
		Send stored DL_1 only static to plane

		Until wp_list[index] is crossed(wpno > 1):
			Do nothing
		Index = index + 1
				
		Localize
		Plan
		Smooth
		Update @vehicle_wps
		Upload @vehicle_wps

		While distance to wp_list[index] > TBD [m]:
			Localize
			Check new object locations against predicted path
			If (path is bad)
				While (new planned path is still bad)
					Plan
						Smooth
						If path is still bad
						Block more
						Else 
							Break

					Update @vehicle_wps
					Upload @vehicle_wps


		# run again until at end of wp list
		plan(index,wp_list)


	def getPath(loc1,loc2,Moving,timeout):
	if (Moving == False):

	else:
		