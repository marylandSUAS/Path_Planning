import sys
import math
from math import pi,sin,cos,atan,atan2
import time
import clr


sys.path.append('C:\\Program Files (x86)\\Mission Planner\\Path_Planning')
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
Home = [38.3652435,-76.5365767,60]

# Competition
Home = [38.1447163,-76.4279848,60]


Leftreset = [38.3660385,-76.5390497,60,True]
LeftPoint = [38.3655800,-76.5391141,60,False]

Rightreset = [38.3645958,-76.5335137,60,False]
RightPoint = [38.3650585,-76.5335137,60,True]


# mission waypoints
# competition
missionGPS = [[38.1507575,-76.4307475,46],
			[38.1496100,-76.4329576,46],
			[38.1420668,-76.4254689,46],
			[38.1437038,-76.4229584,61],
			[38.1455601,-76.4243960,152],
			[38.1439907,-76.4288163,91]]

# southern maryland
# missionGPS = [LeftPoint, RightPoint]

missionWpsPlan = [True]*len(missionGPS)



# initialize coordinate system
cordSystem = Cord_System.Cord_System(Home)

# create avoidance class to control vehicle during obstacle avoidance
missionFunc = missionFunctions.missionTasks(cs,MAV,cordSystem)

# create avoidance class to control vehicle during obstacle avoidance
avoider = Avoider.Avoidance(cs,MAV,cordSystem)


















# in wps
total_List = missionFunc.TakeoffWps
total_Plan = missionFunc.TakeoffPlan
takeoffNum = len(total_List)

# in wps
missionWps = []
for i in missionGPS:
	missionWps.append(cordSystem.GPStoWp(i))
total_List.extend(missionWps)
total_Plan.extend(missionWpsPlan)
missionNum = len(total_List)

# in wps
total_List.extend(missionFunc.dropwps)
total_Plan.extend(missionFunc.dropPlan)
dropNum = len(total_List)

# in wps
total_List.extend(missionFunc.searchGridWps)
total_Plan.extend(missionFunc.searchGridPlan)
searchGridNum = len(total_List)

# in wps
total_List.extend(missionFunc.emergentwps)
total_Plan.extend(missionFunc.emergentPlan)
emergentNum = len(total_List)
# in wps
total_List.extend(missionFunc.offAxiswps)
total_Plan.extend(missionFunc.offAxisPlan)
offAxisNum = len(total_List)

# in wps
total_List.extend(missionFunc.landingwps)
total_Plan.extend(missionFunc.landingPlan)
finalNum = len(total_List)

missionFunc.set_MP_wps(total_List)

MAV.setMode('Auto')



'''
print 'taking off'
avoider.takeoff(missionWps[0])
print 'Waypoints'
avoider.missionWps(missionWps,missionNum,missionFunc.dropwps[0])
print 'Payload'
avoider.droppayload(dropNum,missionFunc.dropwps[len(missionFunc.dropwps)-1],missionFunc.searchGridWps[0])
print 'Grid'
avoider.grid(missionFunc.searchGridWps,searchGridNum,missionFunc.searchGridPlan,missionFunc.emergentwps[0])
print 'Emergent'
avoider.emergent(emergentNum,missionFunc.emergentwps[0],missionFunc.offAxiswps[0])
print 'Off Axis'
avoider.offAxis(offAxisNum,missionFunc.offAxiswps[len(missionFunc.offAxiswps)-1],missionFunc.landingwps[0])
print 'Landing'
'''