# CLASS AVOIDER
import os
import localization
from localization import movingObs
import CheckingAndBlocking
from CheckingAndBlockingNew import Check
import threading
import time
import MissionPlanner
# clr.AddReference("MissionPlanner.Utilities") #includes the Utilities class
from MissionPlanner.Utilities import Locationwp
import MAVLink

class Avoidance:
		

	def __init__(self,start,cs,mav,cord_Sys):
		
		self.Safety_Margin = 6
		self.cruise = 16	
		self.dataPath = 'dlite/flight_information.txt'


		self.cord_System = cord_Sys
		self.MAV = mav

		self.Index = 0
		self.vehicle_wps = []

		self.wp_list = []

		self.Home = start

		self.assuptions = []
		self.logger = None
		self.quit = False

		# self.Bounds = []
		# self.addBounds('dlite/Boundry_File.txt')

		self.StaticObstacles = []
		self.expandedStaticObstacles = []
		self.expandedDynamicObstacles = []
		self.addStaticObstacles('Flight_Logs/static_obstacles.txt')

		self.localizer = movingObs('Flight_Logs/moving_obstacles.txt')


	def addLogger(self,loger):
		self.logger = loger
		self.assuptions = True

	def assumptions(self,pathStillGood,statics,dynamics):
		temp = []

		if(statics != None):
			for ob in statics:
				temp2 = 'AsStatic'+str(ob[0])+' '+str(ob[1])+' '+str(ob[2])+' '+str(ob[3])
				temp.append(temp2)

		if(dynamics != None):
			for ob in dynamics:
				temp2 = 'AsDynamic'+str(ob[0])+' '+str(ob[1])+' '+str(ob[2])+' '+str(ob[3])+' '+str(ob[4])+' '+str(ob[5])+' '+str(ob[6])
				temp.append(temp2)

		if(pathStillGood == False):
			temp.append(' Bad_Path')
		if (self.logger != None):
			self.logger.assuption = temp

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



	# WPlst = list of points to next global wp including global wp
	# TimeToStart = approximate time until first global wp
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



			minus_dist, minus_error = self.localizer.closestApproach(Pos,Vel,Time)
			plus_dist, plus_error = self.localizer.closestApproach(Pos,Vel,Time)
			
			for k in range(len(minus_dist)):
				if (minus_dist[k] < minus_error[k][3]+self.Safety_Margin or plus_dist[k] < plus_error[k][3]+self.Safety_Margin):
					tempOb = [minus_error[0],minus_error[1],minus_error[2],plus_error[0],plus_error[1],plus_error[2],minus_error[3]]
					Important_moving_Obs.append(tempOb)


			Time = Time + dis/self.cruise
			# add time based off angle and time it takes turn
			# could be like turn radius/cruise_speed time sin angle

		return Important_moving_Obs


	def start(self):
		print 'start planning'
		# time.sleep(5)

		self.test()

		# self.plan(self.index)
		print 'finished planning'

	
	#updates vehicle_wps and sends to plane
	def set_vehicle_waypoints(self,wps):
		self.MAV.setWPTotal(len(wps)+1)	
# doesnt know what Locationwp is
		self.MAV.setWP(Locationwp().Set(self.Home[0],self.Home[1],self.Home[2], 16),0,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
		for i in range(len(wps)):
			self.MAV.setWP(Locationwp().Set(wps[i][0],wps[i][1],wps[i][2], 16),1+i,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
			if (i+1 == 1):
				self.MAV.setWPCurrent(1)	
		self.MAV.setMode("Auto")
		self.vehicle_wps = wps


	def get_current_index(self):
		pass
		return self.Index


	def get_current_status(self):
		pass
		return 'Probably Still good'

	def test(self):
		
		# static path and send
		print self.wp_list
		staticPath = self.DL(self.wp_list[self.Index],self.wp_list[self.Index + 1],self.StaticObstacles,[],2)
		print 'found static path'
		print 'static path:'
		print staticPath
		self.set_vehicle_waypoints(staticPath)
		print 'set wps'

		# localize moving obstacles
		important_Dy_Obstacles = self.getMovingObstacles(self.wp_list,0)
		print 'localized important dynamics obstacles'
		# see if it records assumptions right
		self.assumptions(True,None,important_Dy_Obstacles)
		print 'set assumptions'
		# see if check has errors
		is_Bad, expandedStatics, expandedDynamics = Check(self.StaticObstacles,important_Dy_Obstacles,self.vehicle_wps)
		print 'checked'
		print 'is bad: ', is_Bad
		print 'statics: ', expandedStatics
		print 'dynamics: ',expandedDynamics



	def plan(self,index):
		if (self.Index == size(self.wp_list)-1):
			return



		while(cs.wp_dist > 40):
			time.sleep(.1)


			# gets static path for dlite to run off of and to initially set
			staticPath = self.DL(self.wp_list[self.Index],self.wp_list[self.Index + 1],self.StaticObstacles,[],2)
			staticPath.append(self.wp_list[Index-1])
			self.set_vehicle_waypoints(staticPath)

			# DL_1(self.wp_list[index],self.wp_list[index + 1],True)
			

			# wait until reached wp 
			while(self.cs.wpno < 2):
				time.sleep(.02)

			
			# localize moving obstacles
			important_Dy_Obstacles = self.getMovingObstacles(self.vehicle_wps,0)

			
			# if there are moving obstacles blocking the way replan and send.  If not keep static path 
			if (len(important_Dy_Obstacles) != 0):
				
				self.assumptions(True,None,important_Dy_Obstacles)

				dynamic_wps = self.DL(self.wp_list[self.Index-1],self.wp_list[self.Index],self.StaticObstacles,important_Dy_Obstacles,5)
				dynamic_wps.append(self.wp_list[Index-1])
				self.set_vehicle_waypoints(dynamic_wps)


			# while still between wps and manuverable check for collisions.  
			while(self.cs.wp_dist > 40):
				if (self.quit == True):
					return None
				# localize_movingObstacles
				current_path = [self.cord_System.toMeters([self.cs.lat,self.cs.lng,self.cs.alt])]
				current_path.extend(vehicle_wps[(self.cs.wpno-1):])

				important_Dy_Obstacles = self.getMovingObstacles(self,current_path,0)
				self.expandedDynamicObstacles = important_Dy_Obstacles
				
				# checking and blocking.  
				# Check new object locations against predicted path
				# return false True if good and static Obstacles if not
				current_loc = self.cord_System.toMeters([self.cs.lat,self.cs.lng,self.cs.alt])

				self.assumptions(False,None,important_Dy_Obstacles)

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
						if (self.quit == True):
							return None
						current_loc = self.cord_System.toMeters([self.cs.lat,self.cs.lng,self.cs.alt])
						wp_try = self.DL(current_loc,self.wp_list[self.Index],self.expandedStaticObstacles,self.expandedDynamicObstacles,5)
						current_list = [current_loc]
						current_list.extend(wp_try)


						# check if path is still bad
						is_Bad, expandedStatics, expandedStatics = Check(self.expandedStaticObstacles,self.expandedDynamicObstacles,current_list)

						self.assumptions(False,expandedStatics,expandedDynamics)

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
		plan(index)


	def DLAS(self):
		os.system('./dlite/main.exe')
		# os.system('./dlite/smooth.exe')
		print 'Found Path'


	# start,goal,current,static,moving,timeout,expanded 
	# def DL(start,goal,current,staticObstacles,movingObstacles,timeout):
	def DL(self,start,goal,staticObstacles,movingObstacles,timeout):
		current = start
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

			if (movingObstacles != []):
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


		ttp = threading.Thread(target=self.DLAS)
		print 'thread created at: ', time.time()
		ttp.start()
		print 'thread started at: ', time.time()
		ttp.join(timeout=3)
		print 'thread joined at: ', time.time()

# need to check if path finding failed

		nodes = []
		intFile = open('dlite/intermediate_waypoints.txt',"r") 
		intFile.readline()
		dat = intFile.readline().split(" ")	
		while(len(dat) > 1):
			nodes.append([float(dat[0]),float(dat[1]),float(dat[2])])
			dat = intFile.readline().split(" ")
				
		intFile.close()
		return nodes

