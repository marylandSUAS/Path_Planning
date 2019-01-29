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
# import warnings

class Avoidance:


	def __init__(self,mission):
		
		self.Safety_Margin = 30
		self.cruise = 52.5	

		self.turning_radius = 90
		self.Mission = mission
		
		print "initalized avoider"

		
	def staticPlan(self,wp1,heading,wp2):
		
		staticPath = [wp1]
		
		temp_points = self.DL(wp1,wp2,self.StaticObstacles,[],3)
		
		staticPath.extend(temp_points)
		staticPath.append(wp2)
		


	# returns nothing atm
	# start,goal,current,static,moving,timeout,expanded 
	def DL(self,start,goal,staticObstacles,movingObstacles,timeouttaken):
		# currentGPS = startGPS
		# return [[(start[0]+goal[0])/2,(start[1]+goal[1])/2,(start[2]+goal[2])/2]]

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
				print 'first line is', firstline

				if (firstline == 'Changed 1\n'):
					print 'changed 1'
					# print 'first line is: ', firstline

					dat = intermediate_file.readline().split(" ")
					while(len(dat) > 1):
						nodes.append([float(dat[0]),float(dat[1]),float(dat[2])])
						dat = intermediate_file.readline().split(" ")	

					# with open('Path_Planning/dlite/flight_information.txt',"w") as shortfile:
					# 	shortfile.write(str("Update 2 "))
					return nodes

			time.sleep(.02)

		# with open('Path_Planning/dlite/flight_information.txt',"w") as shortfile:
			# shortfile.write(str("Update 2 "))

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


	def totalreplan(self,wp_list,planList):
		# print 'received: ', len(wp)
		# print 'received: ', len(planList)
		# print wp_list

		for k in range(self.cs.wpno,len(wp_list)):
			print 'starting wp no ',k+1,' reading ', planList[k], 'K = ',k

			if planList[k]:
				print wp_list[k]
				wp2 = self.cord_System.WptoMeter(wp_list[k])
				print 'wp2'
				
				if(k == 1):
					while(self.cs.wpno < k):
						print 'waiting for ', k+1
						time.sleep(.25)
					wp1 = self.currentLoc()



				elif(wp_list[k-1].id == 16):
					wp1 = self.cord_System.WptoMeter(wp_list[k-1])
				elif(wp_list[k-2].id == 16):
					wp1 = self.cord_System.WptoMeter(wp_list[k-2])
				elif(wp_list[k-3].id == 16):
					wp1 = self.cord_System.WptoMeter(wp_list[k-3])
				elif(wp_list[k-4].id == 16):
					wp1 = self.cord_System.WptoMeter(wp_list[k-4])
				else:
					wp1 = self.cord_System.WptoMeter(wp_list[k-1])

				print 'wp1'

				staticPath = [wp1]
				temp_points = self.DL(wp1,wp2,self.StaticObstacles,[],3)
				staticPath.extend(temp_points)
				staticPath.append(wp2)

				print 'static path length: ',len(staticPath)-2

				while(self.cs.wpno < k+1):
					print 'waiting for ', k
					time.sleep(.2)

				print 'done waiting for arrival'

				important_Dy_Obstacles = self.getMovingObstacles(staticPath,0)
				finalPath = temp_points

				print 'got obstacles'

				if(len(important_Dy_Obstacles) > 0):
					finalPath = self.DL(self.cord_System.WptoMeter(wp_list[k]),self.cord_System.WptoMeter(wp_list[k+1]),self.StaticObstacles,important_Dy_Obstacles,3)
					print 'got dynamic path'
				else:
					print 'no dynamic needed'

				print 'final path length: ', len(finalPath)
				for wp in finalPath:
					wptemp = [wp[0],wp[1],wp[2]*.3048]
					self.MAV.setGuidedModeWP(self.cord_System.MetertoWp(wptemp))
					self.MAV.setMode('Guided')
					print 'heading toward wp'
					while(True):
						time.sleep(.2)
						tempwp_dist = self.cs.wp_dist
						tempcheck = self.checkbreak()
						print 'waiting for break, dist = ',tempwp_dist, 'check = ',tempcheck
						if(tempwp_dist < 25 or tempcheck):
							break
					print 'exited loop'

				self.MAV.setMode('Auto')
				print 'back to auto'
			print 'finished ',k