import sys
import math
from math import pi,sin,cos,atan,atan2
import time
import threading

import Mission_Testing
import Avoider
import Cord_System
import Current_State_TestClass
import Logger



# Driver

Tasks = ['Takeoff','Navigation','Payload','Off Axis','Search Grid','Emergent Target','Landing']


def main():
	# set home position for takeoff to wherever script is started
	Home = [39.0832638,-76.9035888,100]
	cs = Current_State_TestClass.Current_State_Test_Class()
	resetPoint1 = []
	resetPoint2 = []
	startPoint = []
	print "initalized params"
	
	# initialize coordinate system
	cordSystem = Cord_System.Cord_System(Home)
	print "initalized coords"

	# create avoidance class to control vehicle during obstacle avoidance (Home,cs,MAV)
	avoider = Avoider.Avoidance(Home,cs,None,cordSystem)
	temp_pbs = avoider.getMovingObstacles([[-150,0,100],[150,0,100]],0)
	print temp_pbs
	print "initalized avoider"

	k = 0
	logFile = 'Flight_Logs/Paper_Flight_Record' + str(k+1) + '.txt'
	logger = Logger.logger(cs,cordSystem,logFile,avoider.localizer,'Flight_Logs/static_obstacles.txt') 
	avoider.addLogger(logger)
	print "added logger"

	logger.startlogging() 
	time.sleep(3)
	logger.stoplogging()	

main()
