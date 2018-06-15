import sys
import math
from math import pi,sin,cos,atan,atan2
import time
import clr


sys.path.append('C:\\Program Files (x86)\\Mission Planner\\Path_Planning')
sys.path.append('C:\\Python27\\Lib')

# import threading




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


# Competition
Home = [38.1447163,-76.4279848,60]


# mission waypoints
# competition
missionGPS = [[38.145314,-76.429119,200],
			[38.149222,-76.429483,300],
			[38.150433,-76.430856,300],
			[38.148950,-76.432286,300],
			[38.147011,-76.430642,400],
			[38.143783,-76.431994,200]]

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

'''
temp = [38.1449526,-76.4285803,200]
total_Plan.append(temp)
total_Plan.append(True)
'''

# in wps
total_List.extend(missionFunc.emergentwps)
total_Plan.extend(missionFunc.emergentPlan)
emergentNum = len(total_List)

'''
temp = [38.1449526,-76.4285803,200]
total_Plan.append(temp)
total_Plan.append(True)
'''

# in wps
total_List.extend(missionFunc.offAxiswps)
total_Plan.extend(missionFunc.offAxisPlan)
offAxisNum = len(total_List)

'''
temp = [38.1449526,-76.4285803,200]
total_Plan.append(temp)
total_Plan.append(True)
'''

# in wps
total_List.extend(missionFunc.landingwps)
total_Plan.extend(missionFunc.landingPlan)
finalNum = len(total_List)

print 'Mission length: ', len(total_List), ' ',len(total_Plan)

# print total_List

# missionFunc.set_MP_wps(total_List)

missionFunc.set_MP_wps(missionFunc.offAxiswps)

'''
MAV.setMode('Auto')
# print total_List
while cs.wpno < len(total_List):
	# try:
	avoider.totalreplan(total_List,total_Plan)
	# except:
		# print 'something failed trying again'
'''