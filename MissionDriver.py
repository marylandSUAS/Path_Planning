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


# import Mission_Testing
import Avoider
import Cord_System
import missionFunctions as MF

def speak(strin):
	print strin
	MissionPlanner.MainV2.speechEngine.SpeakAsync(strin)





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

# create avoidance class to control vehicle during obstacle avoidance
avoider = Avoider.Avoidance(cs,MAV,cordSystem)
print "initalized avoider"

# create avoidance class to control vehicle during obstacle avoidance
missionFunc = MF.missionTasks(cs,MAV,cordSystem)
print "initalized mission functions"


resetPoint1 = cordSystem.toMeters([39.0835220,-76.9064641,100.0,False])
resetPoint2 = cordSystem.toMeters([39.0828391,-76.9069147,100.0,False])
startPoint = cordSystem.toMeters([39.0826392,-76.9064212,100.0,False])
endpoint = cordSystem.toMeters([39.0836885,-76.9029611,100.0, True])



# logFile = 'Paper_Flight_Record' + str(k+1) + '.txt'
# logger = Logger.logger(cs,cordSystem,logFile,None,'PathPlanning/Flight_Logs/static_obstacles.txt') 
# avoider.addLogger(logger)

avoider.wp_list = [startPoint, endpoint]

# logger.startlogging() 



missionFunc.offAxis()
missionFunc.payloadDrop()

# avoider.start()

# logger.stoplogging() 