# CLASS AVOIDER

class Avoidance:
		

	def __init__(self,start,cs,MAV,cord_Sys):
		
		Safety_Margin = 6
		cruise = 16	
		dataPath = 'dlite/flight_information.txt'
		self.cord_System = cord_Sys

		self.Index = 0
		self.vehicle_wps = []

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
				
				temp = self.cord_System.toMeters([float(dat[1]),float(dat[2]),float(dat[3])])

				temp.append(float(dat[4]))
				self.StaticObstacles.append(temp)

		# print self.StaticObstacles

	def addBounds(self,bounds_file):
		lngth = self.file_len_Loc(bounds_file)

		with open(bounds_file,"r") as BFile:
			for i in range(lngth):
				dat = BFile.readline().split(" ")
				
				temp = self.cord_System.toMeters([float(dat[1]),float(dat[2]),float(dat[3])])

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
		self.vehicle_wps = wps


	

	def get_current_index(self):
		pass
		return self.Index


	def plan(self,index,wp_list):
		if (index == size(wp_list)-1):
			return
		while(distance to wp_list[index] > TBD [m]):
			time.sleep(.1)

			staticPath = self.DL(wp_list[index],wp_list[index + 1], [],2)
			self.set_vehicle_waypoints(staticPath)

			# DL_1(wp_list[index],wp_list[index + 1],True)
			

			while(self.cs.wpno < 2):
				time.sleep(.02)

			
			important_Dy_Obstacles = self.getMovingObstacles(self,staticPath,0)
			
			dynamic_wps = self.DL(wp_list[index],wp_list[index + 1],important_Dy_Obstacles,5)

			self.set_vehicle_waypoints(dynamic_wps)

			while(self.cs.wp_dist > TBD [m]):
				important_Dy_Obstacles = self.getMovingObstacles(self,vehicle_wps,0)

				# checking and blocking
				is_Bad = Check new object locations against predicted path

				if(is_Bad):
					while(is_Bad)
						
						wp_try = self.DL(self.cord_System.toMeters([cs.lat,cs.lng,cs.alt]),wp_list[index + 1],important_Dy_Obstacles,5)
						

						if(check if path is still bad)
							Block more
						else 
							break

					self.set_vehicle_waypoints(wp_try)
				time.sleep(.25)

		self.Index = self.Index + 1

		# run again until at end of wp list
		plan(index,wp_list)


	def DL(loc1,loc2,moving_obstacles,timeout):
		set up flightinfo.txt
		run dlite
		Smooth
		return []