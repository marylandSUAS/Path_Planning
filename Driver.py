import sys
sys.path.append('C:\Python27\Lib')
sys.path.append('C:\Users\derek_000\Documents\Documents\MUAS\Path_Planning')
import math
from math import pi,sin,cos,atan,atan2
import clr
import time
import System
from System import Byte

import threading
import Logger



clr.AddReference("MissionPlanner")
import MissionPlanner
clr.AddReference("MissionPlanner.Utilities") #includes the Utilities class
from MissionPlanner.Utilities import Locationwp
clr.AddReference("MAVLink") # includes the Utilities class
import MAVLink
MissionPlanner.MainV2.speechEnable = True


# import Mission_Testing
import Avoider
import Cord_System
import functions

def speak(strin):
	print strin
	MissionPlanner.MainV2.speechEngine.SpeakAsync(strin)







def main():
	# set home position for takeoff to wherever script is started
	Home = [39.0829973,-76.9045262,100.0]

	resetPoint1 = [39.0835220,-76.9064641,100.0,False]
	resetPoint2 = [39.0828391,-76.9069147,100.0,False]
	startPoint = [39.0826392,-76.9064212,100.0,False]
	endpoint = [39.0836885,-76.9029611,100.0, True]

	# mission = Mission_Testing.Mission('FreeState')

	# initialize coordinate system
	cordSystem = Cord_System.Cord_System(Home)
	print "initalized coords"

	resetPoint1 = cordSystem.toMeters([39.0835220,-76.9064641,100.0,False])
	resetPoint2 = cordSystem.toMeters([39.0828391,-76.9069147,100.0,False])
	startPoint = cordSystem.toMeters([39.0826392,-76.9064212,100.0,False])
	endpoint = cordSystem.toMeters([39.0836885,-76.9029611,100.0, True])

	# create avoidance class to control vehicle during obstacle avoidance (Home,cs,MAV)
	# avoider = avoidance(Home,cs,MAV,cord_System)
	avoider = Avoider.Avoidance(cs,MAV,cordSystem)
	print "initalized avoider"

	# return
	# define test mission
	# Missions = Mission('FreeState') 

	number_of_tests = 1
	for k in range(number_of_tests):

		# logFile = 'Paper_Flight_Record' + str(k+1) + '.txt'
		# logger = Logger.logger(cs,cordSystem,logFile,None,'PathPlanning/Flight_Logs/static_obstacles.txt') 
		# avoider.addLogger(logger)
		# print "added logger"

		avoider.wp_list = [startPoint, endpoint]
		# avoider.test()
		# AvoiderMethod = threading.Thread(target=avoider.start)
		# print 'added avoider thread'
		avoider.set_vehicle_waypoints([resetPoint1,resetPoint2,startPoint])
		while(cs.wpno < 2):
			Script.Sleep(1000)
		
		avoider.start()
		# avoider.test()
		
		# logger.startlogging() 
		# AvoiderMethod.start()
		# print "Avoider Running"

		# monitor(AvoiderMethod,avoider)
		# print 'finished monitoring'
		return
		
		avoider.set_vehicle_waypoints([resetPoint1,resetPoint2,startPoint])
		print 'returning'
		
		
		while(cs.wpno < 2):
			Script.Sleep(1000)
			print 'waiting until reached wp 2'
		# logger.stoplogging()


		while(cs.wpno < 3):
			Script.Sleep(1000)
			
		print 'reached wp, would restart now'
		
main()