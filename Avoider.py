# CLASS AVOIDER
# import os
import localization
from localization import movingObs
# import CheckingAndBlockingNew
from CheckingAndBlockingNew import Check
import threading
import time

import MissionPlanner
from MissionPlanner.Utilities import Locationwp
import MAVLink

import math

class Avoidance:


	def __init__(self,CS,mav,cord_Sys):
		
		self.Safety_Margin = 30
		self.cruise = 52.5	
		self.dataPath = 'Path_Planning/dlite/flight_information.txt'


		self.cord_System = cord_Sys
		self.MAV = mav
		self.cs = CS
		self.Home = cord_Sys.Home

		self.Index = 0
		self.vehicle_wps = []

		self.wp_list = []

		self.assuptions = []
		self.logger = None
		self.pause = False
		self.quit = False

		self.printLocation = True
		self.printLocThread = threading.Thread(target=self.printLoc)
		self.printLocThread.start()
		
		self.StaticObstacles = []
		self.addStaticObstacles('Path_Planning/data/static_obstacles.txt')

		self.localizer = movingObs('Path_Planning/data/moving_obstacles.txt')

		self.Bounds = []
		self.addBounds()

		print "initalized avoider"


	def currentLoc(self):
		pass
		return self.cord_System.toMeters([self.cs.lat,self.cs.lng,self.cs.alt])

	def printLoc(self):
		timestart = time.time()
		while(self.printLocation and time.time()-timestart < 60):
			
			loc = self.currentLoc()

			senarioFile = open('Path_Planning/GUI/current_state.txt',"w")
			senarioFile.write(str(loc[0]))
			senarioFile.write(str(' '))
			senarioFile.write(str(loc[1]))
			senarioFile.write(str(' '))
			senarioFile.write(str(loc[2]))
			senarioFile.write(str(' '))
			senarioFile.write(str(self.cs.airspeed))
			senarioFile.write(str(' '))
			senarioFile.write(str(self.cs.wpno))
			senarioFile.close()
			
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

	def checkStaticOnly(self):
		OFile = open('Path_Planning/GUI/static_bool.txt',"r")
		dat = OFile.readline().split(" ")
		stat = False
		if(dat[0] == 1):
			stat = True
		
		OFile.close()
		return stat

	def addStaticObstacles(self,static_file):

		OFile = open(static_file,"r")
		dat = OFile.readline().split(" ")
		# print dat
		while(len(dat) > 3):

			temp = [float(dat[0]),float(dat[1]),float(dat[2])]
			temp = self.cord_System.toMeters([float(dat[0]),float(dat[1]),float(dat[2])])
			temp.append(float(dat[3]))
			self.StaticObstacles.append(temp)

			dat = OFile.readline().split(" ")
			# print dat
		
		OFile.close()

		OFile = open('Path_Planning/GUI/static_obstacles.txt',"w")
		for i in range(len(self.StaticObstacles)):
			if(i != 0):
				OFile.write(str('\n'))
			OFile.write(str(self.StaticObstacles[i][0]))
			OFile.write(str(' '))
			OFile.write(str(self.StaticObstacles[i][1]))
			OFile.write(str(' '))
			OFile.write(str(self.StaticObstacles[i][2]))
			OFile.write(str(' '))
			OFile.write(str(self.StaticObstacles[i][3]))
		
		OFile.close()

	def addBounds(self):

		'''
		# flying field 		
		self.Bounds.append(self.cord_System.toMeters([38.3652183,-76.5409541,50]))
		self.Bounds.append(self.cord_System.toMeters([38.3641457,-76.5325481,50]))
		self.Bounds.append(self.cord_System.toMeters([38.3660637,-76.5320653,50]))
		self.Bounds.append(self.cord_System.toMeters([38.3672919,-76.5409005,50]))


		'''
		# competition
		self.Bounds.append(self.cord_System.toMeters([38.1466738,-76.4279151,0.0]))
		self.Bounds.append(self.cord_System.toMeters([38.1512131,-76.4292884,0.0]))
		self.Bounds.append(self.cord_System.toMeters([38.1519386,-76.4314556,0.0]))
		self.Bounds.append(self.cord_System.toMeters([38.1506056,-76.4353824,0.0]))
		self.Bounds.append(self.cord_System.toMeters([38.1481082,-76.4330006,0.0]))
		self.Bounds.append(self.cord_System.toMeters([38.1447501,-76.4327645,0.0]))
		self.Bounds.append(self.cord_System.toMeters([38.1432650,-76.4346743,0.0]))
		self.Bounds.append(self.cord_System.toMeters([38.1404973,-76.4327431,0.0]))
		self.Bounds.append(self.cord_System.toMeters([38.1404973,-76.4260697,0.0]))
		self.Bounds.append(self.cord_System.toMeters([38.1439738,-76.4213920,0.0]))
		self.Bounds.append(self.cord_System.toMeters([38.1471801,-76.4234304,0.0]))
		self.Bounds.append(self.cord_System.toMeters([38.1462857,-76.4264131,0.0]))


		OFile = open('Path_Planning/GUI/boundry.txt',"w")
		for i in range(len(self.Bounds)):
			if(i != 0):
				OFile.write(str('\n'))
			OFile.write(str(self.Bounds[i][0]))
			OFile.write(str(' '))
			OFile.write(str(self.Bounds[i][1]))		
		OFile.close()


		OFile = open('Path_Planning/dlite/boundry.txt',"w")
		for i in range(len(self.Bounds)):
			if(i != 0):
				OFile.write(str('\n'))
			OFile.write(str(self.Bounds[i][0]))
			OFile.write(str(' '))
			OFile.write(str(self.Bounds[i][1]))		
		
		OFile.write(str('\n'))
		OFile.write(str(self.Bounds[0][0]))
		OFile.write(str(' '))
		OFile.write(str(self.Bounds[0][1]))

		for i in reversed(range(len(self.Bounds))):
			OFile.write(str('\n'))
			OFile.write(str(self.Bounds[i][0]))
			OFile.write(str(' '))
			OFile.write(str(self.Bounds[i][1]))			
		OFile.close()

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
				if (minus_dist[k] < minus_error[k][3]+self.Safety_Margin*3 or plus_dist[k] < plus_error[k][3]+self.Safety_Margin*3):
					tempOb = [minus_error[k][0],minus_error[k][1],minus_error[k][2],plus_error[k][0],plus_error[k][1],plus_error[k][2],minus_error[k][3]]
					Important_moving_Obs.append(tempOb)


			Time = Time + dis/self.cruise
			# add time based off angle and time it takes turn
			# could be like turn radius/cruise_speed time sin angle

		OFile = open('Path_Planning/GUI/moving_obstacles_predicted.txt',"w")
		for i in range(len(Important_moving_Obs)):
			if(i != 0):
				OFile.write(str('\n'))
			OFile.write(str(Important_moving_Obs[i][0]))
			OFile.write(str(' '))
			OFile.write(str(Important_moving_Obs[i][1]))
			OFile.write(str(' '))
			OFile.write(str(Important_moving_Obs[i][2]))
			OFile.write(str(' '))
			OFile.write(str(Important_moving_Obs[i][3]))
			OFile.write(str(' '))
			OFile.write(str(Important_moving_Obs[i][4]))
			OFile.write(str(' '))
			OFile.write(str(Important_moving_Obs[i][5]))
			OFile.write(str(' '))
			OFile.write(str(Important_moving_Obs[i][6]))
		OFile.close()

		return Important_moving_Obs

	def start(self):
		print 'start planning'
		
		for wpNum in range(len(self.wp_list)-1):
			self.Index = wpNum+1	
			# print 'waypoint avoidance is', self.wp_list[wpNum+1][3] 
			if(self.wp_list[wpNum+1][3]): 
				if(self.checkStaticOnly()):
					print 'static planning'
					self.staticPlan(self.wp_list[wpNum],self.wp_list[wpNum+1])
				else:
					print 'dynamic planning'
					self.plan(self.wp_list[wpNum],self.wp_list[wpNum+1])
			else:
				print 'not planning'
				self.notPlan(self.wp_list[wpNum],self.wp_list[wpNum+1])
			

		print 'finished planning'
	
	#updates vehicle_wps and sends to plane
	def set_vehicle_waypoints(self,wps):
		self.MAV.setWPTotal(len(wps)+1)	
		self.MAV.setWP(Locationwp().Set(self.Home[0],self.Home[1],self.Home[2], 16),0,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
		for i in range(len(wps)):
			tempcord = self.cord_System.toGPS([wps[i][0],wps[i][1],wps[i][2]])

			self.MAV.setWP(Locationwp().Set(tempcord[0],tempcord[1],tempcord[2],16),1+i,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
			if (i+1 == 1):
				self.MAV.setWPCurrent(1)
		self.MAV.setMode("Auto")

		OFile = open('Path_Planning/GUI/waypoints.txt',"w")
		for i in range(len(wps)):
			if(i != 0):
				OFile.write(str('\n'))
			OFile.write(str(wps[i][0]))
			OFile.write(str(' '))
			OFile.write(str(wps[i][1]))
			OFile.write(str(' '))
			OFile.write(str(wps[i][2]))
		OFile.close()

	def loiter(self):
		self.MAV.setGuidedModeWP(locationwp().Set(self.cs.lat,self.cs.lng,self.cs.alt, 16))
		self.MAV.setMode("Guided")
		while(self.pause):
			time.sleep(.1)
		self.MAV.setMode("Auto")

	def test(self):
		# static path and send

		staticPath = [self.cord_System.WptoMeter()]
		temp_points = self.DL(self.cord_System.WptoMeter(wp1),self.cord_System.WptoMeter(wp2),self.StaticObstacles,[],3)
		staticPath.extend(temp_points)
		staticPath.append(self.cord_System.WptoMeter(wp2))


		while(self.cs.wpno < num+1):
			time.sleep(.05)


		important_Dy_Obstacles = self.getMovingObstacles(staticPath,0)
		finalPath = temp_points
			
		if(len(important_Dy_Obstacles) > 0):
			finalPath = self.DL(self.cord_System.WptoMeter(wp1),self.cord_System.WptoMeter(wp2),self.StaticObstacles,important_Dy_Obstacles,3)
			
			for wp in finalPath:
				self.MAV.setGuidedModeWP(self.cord_System(MetertoWp(wp)))
				while(self.cs.wp_dist > 30):
					time.sleep(.05)	
		self.MAV.setMode('Auto')
		while(self.cs.wp_dist > 40 and self.cs.wpno < wp1num+2):
			time.sleep(.05)

	def notPlan(self,wp1,wp2):
		self.set_vehicle_waypoints([wp1,wp2])
		while(self.cs.wpno < 2):
			time.sleep(.01)
		while(self.cs.wp_dist > 40):
			time.sleep(.01)

	def staticPlan(self,wp1,wp2):
		self.set_vehicle_waypoints([wp1,wp2])
		# gets static path for dlite to run off of and to initially set
		staticPath = [wp1]
		temp_points = self.DL(wp1,wp2,self.StaticObstacles,[],3)
		# if(temp_points != []):
		staticPath.extend(temp_points)
		staticPath.append(wp2)
		print 'Total Path in Meters: ',staticPath
		# sends up initial static path before reaching first wp
		self.set_vehicle_waypoints(staticPath)
		while(self.cs.wpno < len(staticPath)):
			time.sleep(.01)
		time.sleep(1)
		while(self.cs.wp_dist > 40):
			time.sleep(.01)

	def dynamicPlan(self, wp1, wp2):
		self.set_vehicle_waypoints([wp1,wp2])
		# gets static path for dlite to run off of and to initially set		
		staticPath = [wp1]
		temp_points = self.DL(wp1,wp2,self.StaticObstacles,[],3)
		# if(temp_points != []):
		staticPath.extend(temp_points)
		staticPath.append(wp2)
		important_Dy_Obstacles = self.getMovingObstacles(staticPath,0)
		
		dyanmicPath = [wp1]
		temp_points = self.DL(wp1,wp2,self.StaticObstacles,important_Dy_Obstacles,3)
		dyanmicPath.extend(temp_points)
		dyanmicPath.append(wp2)
		
		# print 'Total Path in Meters: ',staticPath

		# sends up initial static path before reaching first wp
		self.set_vehicle_waypoints(dyanmicPath)
		while(self.cs.wpno < len(dyanmicPath)):
			time.sleep(.01)
		time.sleep(1)
		while(self.cs.wp_dist > 40):
			time.sleep(.01)

	def plan(self,wp1,wp2):
		# if (self.Index == size(self.wp_list)-1):
			# return

		self.set_vehicle_waypoints([wp1,wp2])
		# gets static path for dlite to run off of and to initially set
		staticPath = [wp1]
		staticPath.extend(self.DL(wp1,wp2,self.StaticObstacles,[],2))
		staticPath.append(wp2)
		# sends up initial static path before reaching first wp
		self.set_vehicle_waypoints(staticPath)
		print 'sent static path of lenth: ',len(staticPath)

		while(self.cs.wpno < 2):
			time.sleep(2)


			# localize moving obstacles
			important_Dy_Obstacles = self.getMovingObstacles(self.vehicle_wps,0)


			# if there are moving obstacles blocking the way replan and send.  If not keep static path 
			if (len(important_Dy_Obstacles) != 0):
				
				self.assumptions(True,None,important_Dy_Obstacles)

				dynamic_wps = self.DL(self.wp_list[self.Index-1],self.wp_list[self.Index],self.StaticObstacles,important_Dy_Obstacles,5)
				dynamic_wps.append(self.wp_list[Index-1])
				self.set_vehicle_waypoints(dynamic_wps)
				print 'found and sent dynamics path'
			else:
				print 'no dynamic obstacles'


		# while still between wps and manuverable check for collisions.  
		while(self.cs.wp_dist > 40):

			if (self.pause == True):
				self.loiter()


			# localize_movingObstacles
			current_path = [self.currentLoc()]
			current_path.extend(vehicle_wps[(self.cs.wpno-1):])

			important_Dy_Obstacles = self.getMovingObstacles(self,current_path,0)
			# self.expandedDynamicObstacles = important_Dy_Obstacles
			
			# checking and blocking.  
			# Check new object locations against predicted path
			# return false True if good and static Obstacles if not
			
			
			self.assumptions(False,None,important_Dy_Obstacles)

			

			is_Bad, expandedStatics, expandedDynamics = Check(self.StaticObstacles,important_Dy_Obstacles,current_path,self.cs.yaw*3.1415/180)
			print 'Checked, is_Bad: ', is_Bad

			# If collision is going to happen replan and check until a workable path is found
			if(is_Bad):
			
				expandedStaticObstacles = self.StaticObstacles
				expandedDynamicObstacles = important_Dy_Obstacles


				# find usable path
				while(is_Bad):
					if (self.quit):
						break
						# return None
					current_loc = self.currentLoc()
					wp_try = self.DL(current_loc,wp2,expandedStaticObstacles,expandedDynamicObstacles,3)
					current_list = [current_loc]
					current_list.extend(wp_try)


					# check if path is still bad
					is_Bad, expandedStatics, expandedStatics = Check(self.staticObstacles,important_Dy_Obstacles,current_list,self.cs.yaw*3.1415/180)

					self.assumptions(False,expandedStatics,expandedDynamics)

					if(is_Bad == False):
						print 'found good path'
						break
				if (self.quit):
					self.quit = False
					is_Bad = False
					break




				self.set_vehicle_waypoints(wp_try)

			time.sleep(.25)

		# reset expanded obstacles each between each wp
		# self.expandedStaticObstacles = self.StaticObstacles
		# self.expandedDynamicObstacles = []


	# returns nothing atm
	# start,goal,current,static,moving,timeout,expanded 
	def DL(self,start,goal,staticObstacles,movingObstacles,timeouttaken):
		# currentGPS = startGPS
		return []

		current = start
		with open('Path_Planning/dlite/flight_information.txt',"w") as flightFile:

			flightFile.write(str("Update 1 "))

			# goal = self.cord_System.toMeters([float(goalGPS[0]),float(goalGPS[1]),float(goalGPS[2])])
			flightFile.write(str('\n'))
			flightFile.write("goal")
			flightFile.write(str(' '))
			flightFile.write(str(goal[0]))
			flightFile.write(str(' '))
			flightFile.write(str(goal[1]))
			flightFile.write(str(' '))
			flightFile.write(str(goal[2]))

			# start = self.cord_System.toMeters([float(startGPS[0]),float(startGPS[1]),float(startGPS[2])])
			flightFile.write(str('\n'))
			flightFile.write("start")
			flightFile.write(str(' '))
			flightFile.write(str(start[0]))
			flightFile.write(str(' '))
			flightFile.write(str(start[1]))
			flightFile.write(str(' '))
			flightFile.write(str(start[2]))

			# current = self.cord_System.toMeters([float(currentGPS[0]),float(currentGPS[1]),float(currentGPS[2])])
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
				flightFile.write(str(ob[2]+self.Safety_Margin))
				flightFile.write(str(' '))
				flightFile.write(str(ob[3]+self.Safety_Margin))

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
					flightFile.write(str(ob[6]+self.Safety_Margin))

		with open('Path_Planning/dlite/intermediate_waypoints.txt',"w") as shortfile:
			shortfile.write(str("Update 0 "))

		# this 
		# time.sleep(2)
		# print 'fake planning'
		# return [2+(start[0]+goal[0])/2,2+(start[1]+goal[1])/2,2+(start[2]+goal[2])/2]

		startTime = time.time()
		nodes = []
		
		while (time.time()-startTime < 3):
			
			with open('Path_Planning/dlite/intermediate_waypoints.txt',"r") as intermediate_file:
				firstline = intermediate_file.readline()
				# print 'first line is', firstline
				if (firstline == 'Changed 1\n'):
					# print 'first line is: ', firstline

					dat = intermediate_file.readline().split(" ")
					while(len(dat) > 1):
						nodes.append([float(dat[0]),float(dat[1]),float(dat[2])])
						dat = intermediate_file.readline().split(" ")	

					with open('dlite/flight_information.txt',"w") as shortfile:
						shortfile.write(str("Update 2 "))
					return nodes

			time.sleep(.02)

		with open('Path_Planning/dlite/flight_information.txt',"w") as shortfile:
			shortfile.write(str("Update 2 "))

		print 'Failed to run'
		return []



	# should be good
	def takeoff(self,waypoint):
		wp = self.cord_System.WptoMeter(waypoint)
		while(self.cs.wpno < 2):
			time.sleep(.05)
		
		staticPath = [self.currentLoc()]
		temp_points = self.DL(self.currentLoc(),wp,self.StaticObstacles,[],3)
		staticPath.extend(temp_points)
		staticPath.append(wp)
		important_Dy_Obstacles = self.getMovingObstacles(staticPath,0)
		finalPath = temp_points
		if(len(important_Dy_Obstacles) > 0):
			temp_points2 = self.DL(staticPath[0],wp,self.StaticObstacles,important_Dy_Obstacles,3)
			finalPath = temp_points2

		for point in finalPath:
			self.setGuidedModeWP(self.cord_System.MetertoWp(point))
			while(self.cs.wp_dist < 30):
				time.sleep(.05)

		self.MAV.setMode('Auto')
		while(self.cs.wp_dist < 30):
				time.sleep(.05)

	# should be good
	def missionWps(self,wp,num,nextWP):
		
		wp.append(nextWP)

		for k in range(len(wp)-1):
			
			staticPath = [self.cord_System.WptoMeter(wp[k])]
			temp_points = self.DL(self.cord_System.WptoMeter(wp[k]),self.cord_System.WptoMeter(wp[k+1]),self.StaticObstacles,[],3)
			staticPath.extend(temp_points)
			staticPath.append(self.cord_System.WptoMeter(wp[k+1]))

			while(self.cs.wpno < num-len(wp)+k+3):
				print 'waiting for ',num-len(wp)+k+3,' on ',self.cs.wpno
				time.sleep(.25)

			important_Dy_Obstacles = self.getMovingObstacles(staticPath,0)
			finalPath = temp_points
			
			if(len(important_Dy_Obstacles) > 0):
				finalPath = self.DL(self.cord_System.WptoMeter(wp[k]),self.cord_System.WptoMeter(wp[k+1]),self.StaticObstacles,important_Dy_Obstacles,3)
			
			for wp in finalPath:
				self.MAV.setGuidedModeWP(self.cord_System.MetertoWp(wp))
				while(self.cs.wp_dist > 30):
					time.sleep(.05)
			self.MAV.setMode('Auto')
			while(self.cs.wp_dist > 40 and self.cs.wpno < num-len(wp)+k+4):
				time.sleep(.05)
	
	# should be good
	def droppayload(self,num,wp1,wp2):
		staticPath = [self.cord_System.WptoMeter(wp1)]
		temp_points = self.DL(self.cord_System.WptoMeter(wp1),self.cord_System.WptoMeter(wp2),self.StaticObstacles,[],3)
		staticPath.extend(temp_points)
		staticPath.append(self.cord_System.WptoMeter(wp2))


		while(self.cs.wpno < num+1):
			time.sleep(.05)


		important_Dy_Obstacles = self.getMovingObstacles(staticPath,0)
		finalPath = temp_points
			
		if(len(important_Dy_Obstacles) > 0):
			finalPath = self.DL(self.cord_System.WptoMeter(wp1),self.cord_System.WptoMeter(wp2),self.StaticObstacles,important_Dy_Obstacles,3)
			
			for wp in finalPath:
				self.MAV.setGuidedModeWP(self.cord_System.MetertoWp(wp))
				while(self.cs.wp_dist > 30):
					time.sleep(.05)	
		self.MAV.setMode('Auto')
		while(self.cs.wp_dist > 40 and self.cs.wpno < wp1num+2):
			time.sleep(.05)

	# should be good
	def grid(wp,num,plan,nextWP):

		while(self.cs.wpno < num-len(wp)+3):
					time.sleep(.05)


		for k in range(len(wp)-1):
			if(plan[k+1]):
				staticPath = [wp[k]]
				temp_points = self.DL(self.cord_System.WptoMeter(wp[k]),self.cord_System.WptoMeter(wp[k+1]),self.StaticObstacles,[],3)
				staticPath.extend(temp_points)
				staticPath.append(self.cord_System.WptoMeter(wp[k+1]))

				important_Dy_Obstacles = self.getMovingObstacles(staticPath,0)
				finalPath = temp_points

				if(len(important_Dy_Obstacles) > 0):
					finalPath = self.DL(self.cord_System.WptoMeter(wp[k]),self.cord_System.WptoMeter(wp[k+1]),self.StaticObstacles,important_Dy_Obstacles,3)

				for wp in finalPath:
					self.MAV.setGuidedModeWP(self.cord_System.MetertoWp(wp))
					while(self.cs.wp_dist > 30):
						time.sleep(.05)

				self.MAV.setMode('Auto')
				while(self.cs.wpno < num-len(wp)+3+k):
					time.sleep(.05)

			else:
				while(self.cs.wpno < num-len(wp)+3+k):
					time.sleep(.05)




		staticPath = [self.cord_System.WptoMeter(wp[len(wp-1)])]
		temp_points = self.DL(self.cord_System.WptoMeter(wp[len(wp-1)]),self.cord_System.WptoMeter(nextWP),self.StaticObstacles,[],3)
		staticPath.extend(temp_points)
		staticPath.append(self.cord_System.WptoMeter(nextWP))

		important_Dy_Obstacles = self.getMovingObstacles(staticPath,0)
		finalPath = temp_points
		
		if(len(important_Dy_Obstacles) > 0):
			finalPath = self.DL(self.cord_System.WptoMeter(wp[len(wp-1)]),self.cord_System.WptoMeter(nextWP),self.StaticObstacles,important_Dy_Obstacles,3)

		for wp in finalPath:
			self.MAV.setGuidedModeWP(self.cord_System.MetertoWp(wp))
			while(self.cs.wp_dist > 30):
				time.sleep(.05)

		self.MAV.setMode('Auto')
		while(self.cs.wpno < num-len(wp)+3+k):
			time.sleep(.05)

	# should be good to go
	def emergent(self,num,wp1,wp2):
		staticPath = [self.cord_System.WptoMeter(wp1)]
		temp_points = self.DL(self.cord_System.WptoMeter(wp1),self.cord_System.WptoMeter(wp2),self.StaticObstacles,[],3)
		staticPath.extend(temp_points)
		staticPath.append(self.cord_System.WptoMeter(wp2))


		while(self.cs.wpno < num+1):
			time.sleep(.05)


		important_Dy_Obstacles = self.getMovingObstacles(staticPath,0)
		finalPath = temp_points
			
		if(len(important_Dy_Obstacles) > 0):
			finalPath = self.DL(self.cord_System.WptoMeter(wp1),self.cord_System.WptoMeter(wp2),self.StaticObstacles,important_Dy_Obstacles,3)
			
			for wp in finalPath:
				self.MAV.setGuidedModeWP(self.cord_System.MetertoWp(wp))
				while(self.cs.wp_dist > 30):
					time.sleep(.05)	
		self.MAV.setMode('Auto')
		while(self.cs.wp_dist > 40 and self.cs.wpno < wp1num+2):
			time.sleep(.05)

	# should be good
	def offaxis(self,num,wp1,wp2):
		staticPath = [self.cord_System.WptoMeter(wp1)]
		temp_points = self.DL(self.cord_System.WptoMeter(wp1),self.cord_System.WptoMeter(wp2),self.StaticObstacles,[],3)
		staticPath.extend(temp_points)
		staticPath.append(self.cord_System.WptoMeter(wp2))


		while(self.cs.wpno < num+1):
			time.sleep(.05)


		important_Dy_Obstacles = self.getMovingObstacles(staticPath,0)
		finalPath = temp_points
			
		if(len(important_Dy_Obstacles) > 0):
			finalPath = self.DL(self.cord_System.WptoMeter(wp1),self.cord_System.WptoMeter(wp2),self.StaticObstacles,important_Dy_Obstacles,3)
			
			for wp in finalPath:
				self.MAV.setGuidedModeWP(self.cord_System.MetertoWp(wp))
				while(self.cs.wp_dist > 30):
					time.sleep(.05)	
		self.MAV.setMode('Auto')
		while(self.cs.wp_dist > 40 and self.cs.wpno < wp1num+2):
			time.sleep(.05)


	def totalreplan(self,wp,planList):
		# print 'received: ', len(wp)
		# print 'received: ', len(planList)

		for k in range(self.cs.wpno-1,len(wp)):
			print 'starting wp no ',k+1,' reading ', planList[k]

			if planList[k]:

				wp2 = self.cord_System.WptoMeter(wp[k])
				print 'wp2'
				
				if(k == 1):
					while(self.cs.wpno < k+1):
						print 'waiting for ', k
						time.sleep(.05)
					wp1 = self.currentLoc()

				elif(wp[k-1].id == 16):
					wp1 = self.cord_System.WptoMeter(wp[k-1])
				elif(wp[k-2].id == 16):
					wp1 = self.cord_System.WptoMeter(wp[k-2])
				elif(wp[k-3].id == 16):
					wp1 = self.cord_System.WptoMeter(wp[k-3])
				elif(wp[k-4].id == 16):
					wp1 = self.cord_System.WptoMeter(wp[k-4])
				else
					wp1 = self.cord_System.WptoMeter(wp[k-1])

				print 'wp1'

				staticPath = [wp1]
				temp_points = self.DL(wp1,wp2,self.StaticObstacles,[],3)
				staticPath.extend(temp_points)
				staticPath.append(wp2)

				print 'static path: ',staticPath

				while(self.cs.wpno < k+1):
					print 'waiting for ', k
					time.sleep(.05)

				print 'done waiting for arrival'

				important_Dy_Obstacles = self.getMovingObstacles(staticPath,0)
				finalPath = temp_points

				print 'got obstacles'

				if(len(important_Dy_Obstacles) > 0):
					finalPath = self.DL(self.cord_System.WptoMeter(wp[k]),self.cord_System.WptoMeter(wp[k+1]),self.StaticObstacles,important_Dy_Obstacles,3)
					print 'got dynamic path'
				else:
					print 'no dynamic needed'	

				for wp in finalPath:
					self.MAV.setGuidedModeWP(self.cord_System.MetertoWp(wp))
					print 'heading toward wp'
					while(self.cs.wp_dist > 100):
						time.sleep(.05)

				self.MAV.setMode('Auto')
				print 'back to auto'
			print 'finished ',k
				
				
			
