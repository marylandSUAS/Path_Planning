
import sys
sys.path.append('C:\Python27\Lib')
sys.path.append('C:\Users\derek_000\Documents\Documents\MUAS\Path Planning')
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


import Mission_Testing
import Avoider
import Cord_System


# Driver

Tasks = ['Takeoff','Navigation','Payload','Off Axis','Search Grid','Emergent Target','Landing']



def run(avoider, Cord_System):
	pass


def monitor(AvoiderMethod,avoider):
	while(AvoiderMethod.isAlive()):
		print 'Index:, ',avoider.Index
		# print 'Assumptions: '
		# print avoider.assumptions
		# if (avoider.assumptions != []):
		# 	for assum in avoider.assumptions:
		# 		print assum
		# else:
		# 	print 'None'
		
		time.sleep(.5)

def main():
	# set home position for takeoff to wherever script is started
	Home = [39.0829973,-76.9045262,100]
	resetPoint1 = [39.0835220,-76.9064641,100,False]
	resetPoint2 = [39.0828391,-76.9069147,100,False]
	startPoint = [39.0826392,-76.9064212,100,False]
	# initialize coordinate system
	cordSystem = Cord_System.Cord_System(Home)
	print "initalized coords"


	# create avoidance class to control vehicle during obstacle avoidance (Home,cs,MAV)
	# avoider = avoidance(Home,cs,MAV,cord_System)
	avoider = Avoider.Avoidance(Home,cs,MAV,cordSystem)
	print "initalized avoider"

	# return
	# define test mission
	# Missions = Mission('FreeState') 

	number_of_tests = 1
	for k in range(number_of_tests):
		# thread this
		# logFile = 'Paper_Flight_Record' + str(k+1) + '.txt'
		# logger = Logger.logger(cs,cordSystem,logFile,None,'Flight_Logs/static_obstacles.txt') 
		# avoider.addLogger(logger)
		# print "added logger"

		avoider.wp_list = [resetPoint1,resetPoint2,startPoint]
		AvoiderMethod = threading.Thread(target=avoider.start)
		print 'added avoider thread'

		# logger.startlogging() 
		AvoiderMethod.start()
		print "Avoider Running"

		monitor(AvoiderMethod,avoider)
		print 'finished monitoring'
		avoider.set_vehicle_waypoints([resetPoint1,resetPoint2,startPoint])
		print 'returning'
		
		
		while(cs.wpno < 2):
			Script.Sleep(1000)

		# logger.stoplogging()

		while (cs.wpno < 4):
			Script.Sleep(1000)
		return




main()