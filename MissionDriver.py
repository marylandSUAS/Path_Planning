import sys
import math
from math import pi,sin,cos,atan,atan2
import time
import clr


sys.path.append('C:\\Users\\imaging2.0\\Documents\\MUAS-18\\Path_Planning\\Path_Planning')
sys.path.append('C:\\Python27\\Lib')

import threading




clr.AddReference("MissionPlanner")
import MissionPlanner
clr.AddReference("MissionPlanner.Utilities") #includes the Utilities class
from MissionPlanner.Utilities import Locationwp
clr.AddReference("MAVLink") # includes the Utilities class
import MAVLink
MissionPlanner.MainV2.speechEnable = True



import Avoider
import Cord_System
import missionFunctions


def speak(strin):
	print strin
	MissionPlanner.MainV2.speechEngine.SpeakAsync(strin)


# Southern Maryland Flying Field
Home = [39.0829973,-76.9045262,100.0]
LeftPoint = [38.3656767,-76.5390015,50,True]
RightPoint = [38.3651047,-76.5335941,100,True]


# mission waypoints
# competition
missionWps = [[38.1507575,-76.4307475,46],
			[38.1496100,-76.4329576,46],
			[38.1420668,-76.4254689,46],
			[38.1437038,-76.4229584,61],
			[38.1455601,-76.4243960,152],
			[38.1439907,-76.4288163,91]]

# southern maryland
missionWps = [LeftPoint, RightPoint]



# initialize coordinate system
cordSystem = Cord_System.Cord_System(Home)

# create avoidance class to control vehicle during obstacle avoidance
avoider = Avoider.Avoidance(cs,MAV,cordSystem)

# create avoidance class to control vehicle during obstacle avoidance
missionFunc = missionFunctions.missionTasks(cs,MAV,cordSystem)



# in wps
total_List = [missionFunc.TakeoffWps]
takeoffNum = len(total_List)

# in gps
for i in missionWps:
	total_List.append(cordSystem.GPStoWp(i))
missionNum = len(total_List)

# in wps
total_List.append(missionFunc.dropwps)
dropNum = len(total_List)

# in wps
total_List.append(missionFunc.searchGridWps)
searchGridNum = len(total_List)

# in wps
total_List.append(missionFunc.emergentwps)
emergentNum = len(total_List)

# in wps
total_List.append(missionFunc.offAxiswps)
offAxisNum = len(total_List)

# in wps
total_List.append(missionFunc.landingwps)
finalNum = len(total_List)

missionFunc.set_MP_wps(total_List)

# avoider.wp_list = [startPoint, endpoint]


# missionFunc.takeoff(Home)
# missionFunc.offAxis()
# missionFunc.payloadDrop()
# missionFunc.Land()


# avoider.start()

