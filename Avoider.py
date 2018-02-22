# CLASS AVOIDER
import os
import localization
import CheckingAndBlocking
import multiprocessing
from multiprocessing import Process

class Avoidance:
		

	def __init__(self,start,cs,MAV,cord_Sys):
		
		Safety_Margin = 6
		cruise = 16	
		dataPath = 'dlite/flight_information.txt'
		self.cord_System = cord_Sys

		self.Index = 0
		self.vehicle_wps = []

		self.Home = start


		# self.Bounds = []
		# self.addBounds('dlite/Boundry_File.txt')

		self.StaticObstacles = []
		self.expandedStaticObstacles = []
		self.expandedDynamicObstacles = []
		self.addStaticObstacles('Flight_Logs/static_obstacles.txt')

		# self.localizer = movingObs('Flight_Logs/moving_obstacles.txt')


	def addStaticObstacles(self,static_file):

		OFile = open(static_file,"r")
		dat = OFile.readline().split(" ")
		print dat
		while(len(dat) > 3):

			temp = self.cord_System.toMeters([float(dat[0]),float(dat[1]),float(dat[2])])
			temp.append(float(dat[3]))
			self.StaticObstacles.append(temp)

			dat = OFile.readline().split(" ")
			print dat
		
		OFile.close()

	def addBounds(self,bounds_file):
		lngth = self.file_len_Loc(bounds_file)

		BFile = open(bounds_file,"r")
		dat = BFile.readline().split(" ")

		while(len(dat) > 3):
			temp = self.cord_System.toMeters([float(dat[1]),float(dat[2]),float(dat[3])])
			self.Bounds.append(temp)
			dat = BFile.readline().split(" ")
				
		BFile.close()
		# print self.StaticObstacles


	def getMovingObstacles(self,WPlst,TimeToStart):
		Time = 0	# dist_to_first_wp/self.cruise 
		timeError = 1

		Important_moving_Obs = []
		# Steps through each dis between wps and looks for collisions
		for i in range(len(WPlst)-1):
			Pos = WPlst[i]
			dx = WPlst[i+1][0]-WPlst[i][0]
			dy = WPlst[i+1][1]-WPlst[i][1]
			dz = WPlst[i+1][2]-WPlst[i][2]
			dis = (dx**2+dy**2+dz**2)**.5

			Vel = [dx*self.cruise/dis,dy*self.cruise/dis,dz*self.cruise/dis]

			minus_error = self.localizer.closestApproach(Pos,Vel,Time)
			plus_error = self.localizer.closestApproach(Pos,Vel,Time)

			tempOb = [minus_error[0],minus_error[1],minus_error[2],plus_error[0],plus_error[1],plus_error[2],plus_error[3],]
			Important_moving_Obs.append(tempOb)

			Time = Time + dis/self.cruise
			# add time based off angle and time it takes turn
			# could be like turn radius/cruise_speed time sin angle

		return ImportantmovObs


	def start():
		pass
		plan(self.index,wp_list)
	
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


	def get_current_status(self):
		pass
		return 'Probably Still good'


	def plan(self,index,wp_list):
		if (self.Index == size(wp_list)-1):
			return



		while(cs.wp_dist > 40):
			time.sleep(.1)


			# gets static path for dlite to run off of and to initially set
			staticPath = self.DL(wp_list[self.Index],wp_list[self.Index + 1],self.StaticObstacles,[],2)
			self.set_vehicle_waypoints(staticPath)

			# DL_1(wp_list[index],wp_list[index + 1],True)
			

			# wait until reached wp 
			while(self.cs.wpno < 2):
				time.sleep(.02)

			
			# localize moving obstacles
			important_Dy_Obstacles = self.getMovingObstacles(self,staticPath,0)

			# if there are moving obstacles blocking the way replan and send.  If not keep static path 
			if (len(important_Dy_Obstacles) != 0):
				dynamic_wps = self.DL(wp_list[self.Index],wp_list[self.Index + 1],self.StaticObstacles,important_Dy_Obstacles,5)
				self.set_vehicle_waypoints(dynamic_wps)


			# while still between wps and manuverable check for collisions.  
			while(self.cs.wp_dist > 40):

				# localize_movingObstacles
				important_Dy_Obstacles = self.getMovingObstacles(self,vehicle_wps,0)
				self.expandedDynamicObstacles = important_Dy_Obstacles
				
				# checking and blocking.  
				# Check new object locations against predicted path
				# return false True if good and static Obstacles if not
				current_loc = self.cord_System.toMeters([cs.lat,cs.lng,cs.alt])


				current_list.extend(self.vehicle_wps[(len(self.vehicle_wps)-cs.wpno):])
# this is wrong, should be checking remainder of waypoints not vehicle wps
# fix the cs.wpno part of this

				is_Bad, expandedStatics, expandedDynamics = Check(self.StaticObstacles,important_Dy_Obstacles,self.vehicle_wps)


				# If collision is going to happen replan and check until a workable path is found
				if(is_Bad):
					self.expandedStaticObstacles = expandedStatics
					self.expandedDynamicObstacles = expandedDynamics

					# find usable path
					while(is_Bad):
						
						current_loc = self.cord_System.toMeters([cs.lat,cs.lng,cs.alt])
						wp_try = self.DL(current_loc,wp_list[self.Index + 1],self.expandedStaticObstacles,self.expandedDynamicObstacles,5)
						current_list = [current_loc]
						current_list.extend(wp_try)


						# check if path is still bad
						is_Bad, expandedStatics, expandedStatics = Check(self.expandedStaticObstacles,self.expandedDynamicObstacles,current_list)

						if(is_Bad == False):
							break
						else:
							self.expandedStaticObstacles = expandedStatics
							self.expandedDynamicObstacles = expandedDynamics

					self.set_vehicle_waypoints(wp_try)
				time.sleep(.25)

		self.Index = self.Index + 1

		# reset expanded obstacles each between each wp
		self.expandedStaticObstacles = self.StaticObstacles
		self.expandedDynamicObstacles = []

		# run again until at end of wp list
		plan(index,wp_list)


	def DLAS(self):
		os.system('./dlite/main.exe')
		# os.system('./dlite/smooth.exe')
		print 'Found Path'


	# start,goal,current,static,moving,timeout,expanded 
	def DL(start,goal,current,staticObstacles,movingObstacles,timeout):

		with open('dlite/flight_information.txt',"w") as flightFile:

			flightFile.write(str("Update 1"))

			flightFile.write(str('\n'))
			flightFile.write("goal")
			flightFile.write(str(' '))
			flightFile.write(str(goal[0]))
			flightFile.write(str(' '))
			flightFile.write(str(goal[1]))
			flightFile.write(str(' '))
			flightFile.write(str(goal[2]))

			flightFile.write(str('\n'))
			flightFile.write("start")
			flightFile.write(str(' '))
			flightFile.write(str(start[0]))
			flightFile.write(str(' '))
			flightFile.write(str(start[1]))
			flightFile.write(str(' '))
			flightFile.write(str(start[2]))

			flightFile.write(str('\n'))
			flightFile.write("current")
			flightFile.write(str(' '))
			flightFile.write(str(current[0]))
			flightFile.write(str(' '))
			flightFile.write(str(current[1]))
			flightFile.write(str(' '))
			flightFile.write(str(current[2]))

			for ob in staticObstacles:
				flightFile.write(str('\n'))
				flightFile.write("static")
				flightFile.write(str(' '))
				flightFile.write(str(ob[0]))
				flightFile.write(str(' '))
				flightFile.write(str(ob[1]))
				flightFile.write(str(' '))
				flightFile.write(str(ob[2]))
				flightFile.write(str(' '))
				flightFile.write(str(ob[3]))

			if (moving):
				for ob in movingObstacles:
					flightFile.write(str('\n'))
					flightFile.write("dynamic")
					flightFile.write(str(' '))
					flightFile.write(str(ob[0]))
					flightFile.write(str(' '))
					flightFile.write(str(ob[1]))
					flightFile.write(str(' '))
					flightFile.write(str(ob[2]))
					flightFile.write(str(' '))
					flightFile.write(str(ob[3]))
					flightFile.write(str(' '))
					flightFile.write(str(ob[4]))
					flightFile.write(str(' '))
					flightFile.write(str(ob[5]))
					flightFile.write(str(' '))
					flightFile.write(str(ob[6]))


		ttp = Process(target=DLAS)
		ttp.start()
		ttp.join(timeout=3)

		nodes = []
		intFile = open('dlite/intermediate_waypoints.txt',"r") 
		intFile.readline()
		dat = intFile.readline().split(" ")	
		while(len(dat) > 1):
			nodes.append([float(dat[0]),float(dat[1]),float(dat[2])])
			dat = intFile.readline().split(" ")
				
		intFile.close()
		return nodes

